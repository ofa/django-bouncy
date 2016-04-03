"""Views for the django_bouncy app"""
import json
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

import re
import logging

from django.http import HttpResponseBadRequest, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from django_bouncy.utils import (
    verify_notification, approve_subscription, clean_time
)
from django_bouncy.models import Bounce, Complaint, Delivery
from django_bouncy import signals

VITAL_NOTIFICATION_FIELDS = [
    'Type', 'Message', 'Timestamp', 'Signature',
    'SignatureVersion', 'TopicArn', 'MessageId',
    'SigningCertURL'
]

VITAL_MESSAGE_FIELDS = [
    'notificationType', 'mail'
]

ALLOWED_TYPES = [
    'Notification', 'SubscriptionConfirmation', 'UnsubscribeConfirmation'
]
logger = logging.getLogger(__name__)


@csrf_exempt
def endpoint(request):
    """Endpoint that SNS accesses. Includes logic verifying request"""
    # pylint: disable=too-many-return-statements,too-many-branches

    # In order to 'hide' the endpoint, all non-POST requests should return
    # the site's default HTTP404
    if request.method != 'POST':
        raise Http404

    # If necessary, check that the topic is correct
    if hasattr(settings, 'BOUNCY_TOPIC_ARN'):
        # Confirm that the proper topic header was sent
        if 'HTTP_X_AMZ_SNS_TOPIC_ARN' not in request.META:
            return HttpResponseBadRequest('No TopicArn Header')

        # Check to see if the topic is in the settings
        # Because you can have bounces and complaints coming from multiple
        # topics, BOUNCY_TOPIC_ARN is a list
        if (not request.META['HTTP_X_AMZ_SNS_TOPIC_ARN']
                in settings.BOUNCY_TOPIC_ARN):
            return HttpResponseBadRequest('Bad Topic')

    # Load the JSON POST Body
    if isinstance(request.body, str):
        # requests return str in python 2.7
        request_body = request.body
    else:
        # and return bytes in python 3.4
        request_body = request.body.decode()
    try:
        data = json.loads(request_body)
    except ValueError:
        logger.warning('Notification Not Valid JSON: {}'.format(request_body))
        return HttpResponseBadRequest('Not Valid JSON')

    # Ensure that the JSON we're provided contains all the keys we expect
    # Comparison code from http://stackoverflow.com/questions/1285911/
    if not set(VITAL_NOTIFICATION_FIELDS) <= set(data):
        logger.warning('Request Missing Necessary Keys')
        return HttpResponseBadRequest('Request Missing Necessary Keys')

    # Ensure that the type of notification is one we'll accept
    if not data['Type'] in ALLOWED_TYPES:
        logger.info('Notification Type Not Known %s', data['Type'])
        return HttpResponseBadRequest('Unknown Notification Type')

    # Confirm that the signing certificate is hosted on a correct domain
    # AWS by default uses sns.{region}.amazonaws.com
    # On the off chance you need this to be a different domain, allow the
    # regex to be overridden in settings
    domain = urlparse(data['SigningCertURL']).netloc
    pattern = getattr(
        settings, 'BOUNCY_CERT_DOMAIN_REGEX', r"sns.[a-z0-9\-]+.amazonaws.com$"
    )
    if not re.search(pattern, domain):
        logger.warning(
            'Improper Certificate Location %s', data['SigningCertURL'])
        return HttpResponseBadRequest('Improper Certificate Location')

    # Verify that the notification is signed by Amazon
    if (getattr(settings, 'BOUNCY_VERIFY_CERTIFICATE', True)
            and not verify_notification(data)):
        logger.error('Verification Failure %s', )
        return HttpResponseBadRequest('Improper Signature')

    # Send a signal to say a valid notification has been received
    signals.notification.send(
        sender='bouncy_endpoint', notification=data, request=request)

    # Handle subscription-based messages.
    if data['Type'] == 'SubscriptionConfirmation':
        # Allow the disabling of the auto-subscription feature
        if not getattr(settings, 'BOUNCY_AUTO_SUBSCRIBE', True):
            raise Http404
        return approve_subscription(data)
    elif data['Type'] == 'UnsubscribeConfirmation':
        # We won't handle unsubscribe requests here. Return a 200 status code
        # so Amazon won't redeliver the request. If you want to remove this
        # endpoint, remove it either via the API or the AWS Console
        logger.info('UnsubscribeConfirmation Not Handled')
        return HttpResponse('UnsubscribeConfirmation Not Handled')

    try:
        message = json.loads(data['Message'])
    except ValueError:
        # This message is not JSON. But we need to return a 200 status code
        # so that Amazon doesn't attempt to deliver the message again
        logger.info('Non-Valid JSON Message Received')
        return HttpResponse('Message is not valid JSON')

    return process_message(message, data)


def process_message(message, notification):
    """
    Function to process a JSON message delivered from Amazon
    """
    # Confirm that there are 'notificationType' and 'mail' fields in our
    # message
    if not set(VITAL_MESSAGE_FIELDS) <= set(message):
        # At this point we're sure that it's Amazon sending the message
        # If we don't return a 200 status code, Amazon will attempt to send us
        # this same message a few seconds later.
        logger.info('JSON Message Missing Vital Fields')
        return HttpResponse('Missing Vital Fields')

    if message['notificationType'] == 'Complaint':
        return process_complaint(message, notification)
    if message['notificationType'] == 'Bounce':
        return process_bounce(message, notification)
    if message['notificationType'] == 'Delivery':
        return process_delivery(message, notification)
    else:
        return HttpResponse('Unknown Notification Type')


def process_bounce(message, notification):
    """Function to process a bounce notification"""
    mail = message['mail']
    bounce = message['bounce']

    bounces = []
    for recipient in bounce['bouncedRecipients']:
        # Create each bounce record. Add to a list for reference later.
        bounces += [Bounce.objects.create(
            sns_topic=notification['TopicArn'],
            sns_messageid=notification['MessageId'],
            mail_timestamp=clean_time(mail['timestamp']),
            mail_id=mail['messageId'],
            mail_from=mail['source'],
            address=recipient['emailAddress'],
            feedback_id=bounce['feedbackId'],
            feedback_timestamp=clean_time(bounce['timestamp']),
            hard=bool(bounce['bounceType'] == 'Permanent'),
            bounce_type=bounce['bounceType'],
            bounce_subtype=bounce['bounceSubType'],
            reporting_mta=bounce.get('reportingMTA'),
            action=recipient.get('action'),
            status=recipient.get('status'),
            diagnostic_code=recipient.get('diagnosticCode')
        )]

    # Send signals for each bounce.
    for bounce in bounces:
        signals.feedback.send(
            sender=Bounce,
            instance=bounce,
            message=message,
            notification=notification
        )

    logger.info('Logged %s Bounce(s)', str(len(bounces)))

    return HttpResponse('Bounce Processed')


def process_complaint(message, notification):
    """Function to process a complaint notification"""
    mail = message['mail']
    complaint = message['complaint']

    if 'arrivalDate' in complaint:
        arrival_date = clean_time(complaint['arrivalDate'])
    else:
        arrival_date = None

    complaints = []
    for recipient in complaint['complainedRecipients']:
        # Create each Complaint. Save in a list for reference later.
        complaints += [Complaint.objects.create(
            sns_topic=notification['TopicArn'],
            sns_messageid=notification['MessageId'],
            mail_timestamp=clean_time(mail['timestamp']),
            mail_id=mail['messageId'],
            mail_from=mail['source'],
            address=recipient['emailAddress'],
            feedback_id=complaint['feedbackId'],
            feedback_timestamp=clean_time(complaint['timestamp']),
            useragent=complaint.get('userAgent'),
            feedback_type=complaint.get('complaintFeedbackType'),
            arrival_date=arrival_date
        )]

    # Send signals for each complaint.
    for complaint in complaints:
        signals.feedback.send(
            sender=Complaint,
            instance=complaint,
            message=message,
            notification=notification
        )

    logger.info('Logged %s Complaint(s)', str(len(complaints)))

    return HttpResponse('Complaint Processed')


def process_delivery(message, notification):
    """Function to process a delivery notification"""
    mail = message['mail']
    delivery = message['delivery']

    if 'timestamp' in delivery:
        delivered_datetime = clean_time(delivery['timestamp'])
    else:
        delivered_datetime = None

    deliveries = []
    for eachrecipient in delivery['recipients']:
        # Create each delivery 
        deliveries += [Delivery.objects.create(
            sns_topic=notification['TopicArn'],
            sns_messageid=notification['MessageId'],
            mail_timestamp=clean_time(mail['timestamp']),
            mail_id=mail['messageId'],
            mail_from=mail['source'],
            address=eachrecipient,
            # delivery
            delivered_time=delivered_datetime,
            processing_time=int(delivery['processingTimeMillis']),
            smtp_response=delivery['smtpResponse']
        )]

    # Send signals for each delivery.
    for eachdelivery in deliveries:
        signals.feedback.send(
            sender=Delivery,
            instance=eachdelivery,
            message=message,
            notification=notification
        )

    logger.info('Logged %s Deliveries(s)', str(len(deliveries)))

    return HttpResponse('Delivery Processed')
