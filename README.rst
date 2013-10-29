*************
django-bouncy
*************

A way to handle bounce and abuse reports delivered by Amazon's `Simple Notification Service`_ regarding emails sent by `Simple Email Service`_

.. _Simple Notification Service: http://aws.amazon.com/sns/
.. _Simple Email Service: http://aws.amazon.com/ses/


Introduction
------------
When an email is sent via Simple Email Service (SES) Amazon will attempt to deliver your message to the recipient's SMTP server. In some instances, such as when an email address is invalid (a 'Hard Bounce'), a user is on vacation (a 'Soft bounce') or a user marks an email as abusive (spam, phishing, etc) Amazon will pass these responses back to your app via one of two ways: either by forwarding the reply to an email address of your choice (the default) or send a JSON encoded message inside a notification delivered via their Simple Notification Service (SNS).

The purpose of django-bouncy is to act as an endpoint for SES which will confirm that the notification came from Amazon and then properly record the bounce or complaint for use by other apps in a project.


Configuration Options
---------------------
There are multiple configuration options avalable for you to include in your django settings file.

``BOUNCY_TOPIC_ARN`` - A string or list of one or more SNS topics the app is authorized to pay attention to. It is highly recommended you set this setting, especially if you did not disable ``BOUNCY_AUTO_SUBSCRIBE``, as a third party could create their own topic on their own SES account pointed to your django-bouncy endpoint, allowing them to batch create bounces that django-bouncy will recognize as valid. Default: ``None``

``BOUNCY_AUTO_SUBSCRIBE`` - All SNS endpoints must verify with Amazon that they are willing to accept SNS notifications. This is done via a SubscriptionNotification sent when you first add a new endpoint, which will contain a unique temporary URL that must be either polled via either a GET request or passed back to Amazon via the API. By default django-bouncy will acknoledge and confirm with Amazon any subscription request sent to it. It does this by visiting the SubscribeURL provided by a SubscriptionNotification.

If you've already verified your django-bouncy endpoint is active, you can disable this auto-subscription by setting this to ``False``, which will result in django-bouncy returning a 404 error to all new SubscriptionNotifications. Default: ``True``

``BOUNCY_VERIFY_CERTIFICATE`` - As part of the verification process django-bouncy checks all notifications against Amazon's public SES key, which Amazon stores on their servers as part of a .pem certificate. You can disable this certificate check by changing this setting to ``False``. Default: ``True``

``BOUNCY_KEY_CACHE`` - As the URLs for the certificates vary by AWS region and the cerficiates have expiration dates, it is not safe to assume that every notification received will use the same key. In order to avoid unnecessary verification failures when keys are saved and also to reduce slow requests for keys, django-bouncy will request a key the first time it receives a notification then store it in django's cache framework.

You can adjust the cache you wish django-bouncy to store the certificate in by changing this setting. Default: ``default``

``BOUNCY_CERT_DOMAIN_REGEX`` - A string that contains the regular expression that should be used to verify the URL of Amazon's public SNS certificate is indeed hosted on Amazon. The default is ``sns.[a-z0-9\-]+.amazonaws.com$`` (which will match sns.region.amazonaws.com) and it's unlikely you'll need to change this.
