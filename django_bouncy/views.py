"""Views for the django_bouncy app"""
import json
import urllib
import re

from django.http import HttpResponseBadRequest, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings

from django_bouncy.utils import (
    verify_notification, approve_subscription, clean_time
)
from django_bouncy.models import Bounce, Complaint

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

@csrf_exempt
@require_POST
def endpoint(request):
    """Default view endpoint"""
    # pylint: disable=too-many-return-statements

    # If necessary, check that the topic is correct
    if hasattr(settings, 'BOUNCY_TOPIC_ARN'):
        # Confirm that the proper topic header was sent
        if not request.META.has_key('HTTP_X_AMZ_SNS_TOPIC_ARN'):
            return HttpResponseBadRequest('No TopicArn Header')

        # Check to see if the topic is in the settings
        # Because you can have bounces and complaints coming from multiple
        # topics, BOUNCY_TOPIC_ARN can be a string or list
        if (not request.META['HTTP_X_AMZ_SNS_TOPIC_ARN']
            in settings.BOUNCY_TOPIC_ARN):
            return HttpResponseBadRequest('Bad Topic')

    # Load the JSON POST Body
    try:
        data = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest('Not Valid JSON')

    # Ensure that the JSON we're provided contains all the keys we expect
    # Comparison code from http://stackoverflow.com/questions/1285911/
    if not set(VITAL_NOTIFICATION_FIELDS) <= set(data):
        return HttpResponseBadRequest('Request Missing Necessary Keys')

    # Ensure that the type of notification is one we'll accept
    if not data['Type'] in ALLOWED_TYPES:
        return HttpResponseBadRequest('Unknown Notification Type')

    # Confirm that the signing certificate is hosted on a correct domain
    # AWS by default uses sns.{region}.amazonaws.com
    # On the off chance you need this to be a different domain, allow the
    # regex to be overridden in settings
    domain = urllib.urlparse(data['SigningCertURL']).netloc
    pattern = getattr(
        settings, 'BOUNCY_CERT_DOMAIN_REGEX', r"sns.[a-z0-9\-]+.amazonaws.com$"
    )
    if not re.search(pattern, domain):
        return HttpResponseBadRequest('Improper Certificate Location')

    # Verify that the notification is signed by Amazon
    if (getattr(settings, 'BOUNCY_VERIFY_CERTIFICATE', True)
        and not verify_notification(data)):
        return HttpResponseBadRequest('Improper Signature')

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
        return HttpResponse('UnsubscribeConfirmation Not Handled')

    try:
        message = json.loads(data['Message'])
    except ValueError:
        # This message is not JSON. But we need to return a 200 status code
        # so that Amazon doesn't attempt to deliver the message again
        return HttpResponse('Message is not valid JSON')

    return process_message(message, data)


def process_message(message, notification):
    """
    Function to process a JSON message delivered from Amazon
    """
    # Confirm that there are 'notificationType' and 'mail' fields in our message
    if not set(VITAL_MESSAGE_FIELDS) <= set(message):
        # At this point we're sure that it's Amazon sending the message
        # If we don't return a 200 status code, Amazon will attempt to send us
        # this same message a few seconds later.
        return HttpResponse('Missing Vital Fields')

    if message['notificationType'] == 'Complaint':
        return process_complaint(message, notification)
    if message['notificationType'] == 'Bounce':
        return process_bounce(message, notification)
    else:
        return HttpResponse('Unknown Notification Type')


def process_bounce(message, notification):
    """Function to process a bounce notification"""
    mail = message['mail']
    bounce = message['bounce']

    bounces = []
    for recipient in bounce['bouncedRecipients']:
        bounces += [Bounce(
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

    Bounce.objects.bulk_create(bounces)

    return HttpResponse('Bounce Processed')


def process_complaint(message, notification):
    """Function to process a complaint notification"""
    mail = message['mail']
    complaint = message['complaint']

    if complaint.has_key('arrivalDate'):
        arrival_date = clean_time(complaint['arrivalDate'])
    else:
        arrival_date = None

    complaints = []
    for recipient in complaint['complainedRecipients']:
        complaints += [Complaint(
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

    Complaint.objects.bulk_create(complaints)

    return HttpResponse('Complaint Processed')
