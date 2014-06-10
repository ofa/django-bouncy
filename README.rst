*************
Django Bouncy
*************

Django Bouncy is a Django package used to process bounce and abuse reports delivered via Amazon Web Services' `Simple Notification Service`_ regarding emails sent by Amazon's `Simple Email Service`_

.. _Simple Notification Service: http://aws.amazon.com/sns/
.. _Simple Email Service: http://aws.amazon.com/ses/


Introduction
------------
When an email is sent via Simple Email Service (SES) Amazon will attempt to deliver your message to the recipient's SMTP server. In some instances, such as when an email address is invalid (a 'Hard Bounce'), a user is on vacation (a 'Soft bounce'), or a user marks an email as abusive or spam Amazon will pass these responses back to your app via one of two ways: either by forwarding the reply to an email address of your choice (the default) or send a JSON encoded and signed message inside a notification delivered via their Simple Notification Service (SNS).

The purpose of Django Bouncy is to act as an endpoint for SES which will confirm that the notification came from Amazon and then properly record the bounce or complaint for use by other apps in a project.


Installation & Configuration
----------------------------
Installing Django Bouncy is relatively easy.

**Step 1: Add Django Bouncy to your Django App**

Before doing any configuration Amazon it's vital that Django Bouncy is installed in your Django application.

First add ``django_bouncy`` to your application's ``INSTALLED_APPS`` setting.

Then add ``django_bouncy.urls`` to your ``urlpatterns`` found in your app's ``urls.py``

For example, if you'd like to create an endpoint at ``http://yourapp.com/bouncy/`` your ``urls.py`` file would look like this:

::

    from django.conf.urls import patterns, include, url
    urlpatterns = patterns('',
        url(r'^bouncy/', include('django_bouncy.urls', app_name='django_bouncy')),
    )

The next steps involve interacting with AWS through the `AWS Management Console`_.

.. _AWS Management Console: https://console.aws.amazon.com/

**Step 2: Create a new SNS topic.**

Django-Bouncy is reliant on a Simple Notification Service (SNS) ``Topic`` being created and your new Django Bouncy endpoint being set as a subscriber. You can find information in the AWS documentation on how to `Create a SNS Topic`_ 


**Step 3: Ensure that your app is deployed with a valid Django-Bouncy endpoint.**

Because subscribing to a SNS Topic requires a valid receiving endpoint which can reply to SNS when a subscription is created, it's vital that your app be live and Django Bouncy be setup at the URL you intend on having in production.

Note that one of the configuration options you can add to your project's ``settings.py`` is ``BOUNCY_TOPIC_ARN``. This is a list of SNS Topic ARNs that Django-Bouncy will pay attention to when sent a request. While this setting is not required, it's highly recommended that you set this otherwise another AWS client could send bulk fake bounce reports to your app.

**Step 4: Create a new SNS subscription to your topic.**

The AWS documentation does a good job of describing how to `Subscribe a HTTP URL to a SNS topic`_. This URL will be the Django Bouncy endpoint you setup in your ``urls.py``.

When you subscribe to your new SNS topic, Amazon will send a subscription verification request to Django-Bouncy, which Django-Bouncy will immediately verify then reply to. Only verified subscriptions can be sent SNS notifications, so make sure that Django Bouncy is live at the endpoint you choose before taking these steps!

The AWS Control Panel should quickly note that the new endpoint was successfully subscribed. If the status of your new subscription is marked as "Pending Verification" after a few minutes, it's possible that something went wrong with Django Bouncy.

**Step 5. Configure Simple Email Service (SES) to use your new SNS Topic for subscriptions.**

The AWS documentation does a great job explaining how to `Switch your SES Notification Preferences to use SNS`_.

If you'd like to test your new Django Bouncy implementation. Amazon provides a `Mailbox Simulator`_ you can use to send SES email that will return a valid bounce or complaint to Django Bouncy.

.. _Create a SNS Topic: http://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html
.. _Subscribe a HTTP URL to a SNS Topic: http://docs.aws.amazon.com/sns/latest/dg/SubscribeTopic.html
.. _Switch your SES Notification Preferences to use SNS: http://docs.aws.amazon.com/ses/latest/DeveloperGuide/configure-sns-notifications.html
.. _Mailbox Simulator: http://docs.aws.amazon.com/ses/latest/DeveloperGuide/mailbox-simulator.html

Processing Bounces and Complaints
---------------------------------
Django Bouncy exposes valid Bounces and Complaints 2 ways: via Django Bouncy's ``Bounce`` and ``Complaint`` models, as well as via a signal that other parts of your Django application can attach to.

To pull all the bounces from Django Bouncy, you'd simply import the model and make that request

::

    from django_bouncy.models import Bounce

    # Generate a queryset of all bounces Django Bouncy has processed
    all_bounces = Bounce.objects.all()
    # Find all hard bounces
    all_hard_bounces = Bounce.objects.filter(hard=True)


The schema for the ``Bounce`` and ``Complaint`` models are best found by viewing the ``django_bouncy/models.py`` file included with Django Bouncy.

If you'd rather subscribe to the notification, perhaps to create new records in your own ``Unsubscribe`` model, simply attach to the ``feedback`` signal:

::

    from django.dispatch import receiver
    from django_bouncy.models import Bounce
    from django_bouncy.signals import feedback
    from my_app.models import Unsubscribe

    @receiver(feedback, sender=Bounce)
    def process_feedback(sender, **kwargs):
        """Process a bounce received from our email vendor"""
        instance = kwargs['instance']
        if instance.hard:
            Unsubscribe.objects.create(address=instance.address, source='bounce')


Configuration Options
---------------------
There are multiple configuration options avalable for you to include in your django settings file.

``BOUNCY_TOPIC_ARN`` - A list of one or more SNS topics the app is authorized to pay attention to. It is highly recommended you set this setting, especially if you did not disable ``BOUNCY_AUTO_SUBSCRIBE``, as a third party could create their own topic on their own SES account pointed to your Django Bouncy endpoint, allowing them to batch create bounces that Django Bouncy will recognize as valid. Default: ``None``

``BOUNCY_AUTO_SUBSCRIBE`` - All SNS endpoints must verify with Amazon that they are willing to accept SNS notifications. This is done via a SubscriptionNotification sent when you first add a new endpoint, which will contain a unique temporary URL that must be either polled via either a GET request or passed back to Amazon via the API. By default django-bouncy will acknoledge and confirm with Amazon any subscription request sent to it. It does this by visiting the SubscribeURL provided by a SubscriptionNotification.

If you've already verified your Django Bouncy endpoint is active, you can disable this auto-subscription by setting this to ``False``, which will result in Django Bouncy returning a 404 error to all new SubscriptionNotifications. Default: ``True``

``BOUNCY_VERIFY_CERTIFICATE`` - As part of the verification process Django Bouncy checks all notifications against Amazon's public SES key, which Amazon stores on their servers as part of a .pem certificate. You can disable this certificate check by changing this setting to ``False``. Default: ``True``

``BOUNCY_KEY_CACHE`` - As the URLs for the certificates vary by AWS region and the cerficiates have expiration dates, it is not safe to assume that every notification received will use the same key. In order to avoid unnecessary verification failures when keys are saved and also to reduce slow requests for keys, Django Bouncy will request a key the first time it receives a notification then store it in django's cache framework.

You can adjust the cache you wish Django Bouncy to store the certificate in by changing this setting. Default: ``default``

``BOUNCY_CERT_DOMAIN_REGEX`` - A string that contains the regular expression that should be used to verify the URL of Amazon's public SNS certificate is indeed hosted on Amazon. The default is ``sns.[a-z0-9\-]+.amazonaws.com$`` (which will match sns.region.amazonaws.com) and it's unlikely you'll need to change this.


Credits
-------
Django Bouncy was built in-house by `Organizing for Action`_ and the source code is available on the `Django Bouncy GitHub Repository`_.

.. _Organizing for Action: http://www.barackobama.com/
.. _Django Bouncy GitHub Repository: https://github.com/ofa/django-bouncy
