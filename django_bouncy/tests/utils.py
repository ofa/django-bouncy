"""Tests for utils.py in the django-bouncy app"""
from django.conf import settings
from django.dispatch import receiver
try:
    # Python 2.6/2.7
    from mock import Mock, patch
except ImportError:
    # Python 3
    from unittest.mock import Mock, patch

from django_bouncy.tests.helpers import BouncyTestCase, loader
from django_bouncy import utils, signals


class TestVerificationSystem(BouncyTestCase):
    """Test the message verification utilities"""
    @patch('django_bouncy.utils.urlopen')
    def test_grab_keyfile(self, mock):
        """Test the grab_keyfile plugin"""
        responsemock = Mock()
        responsemock.read.return_value = self.pemfile
        mock.return_value = responsemock
        result = utils.grab_keyfile('http://www.fakeurl.com')

        mock.assert_called_with('http://www.fakeurl.com')
        self.assertEqual(result, self.pemfile)

    @patch('django_bouncy.utils.urlopen')
    def test_bad_keyfile(self, mock):
        """Test a non-valid keyfile"""
        responsemock = Mock()
        responsemock.read.return_value = 'Not A Certificate'
        mock.return_value = responsemock

        with self.assertRaises(ValueError) as context_manager:
            utils.grab_keyfile('http://www.fakeurl.com')

        the_exception = context_manager.exception
        self.assertEqual(the_exception.args[0], 'Invalid Certificate File')

    @patch('django_bouncy.utils.grab_keyfile')
    def test_verify_notification(self, mock):
        """Test the verification of a valid notification"""
        mock.return_value = self.pemfile
        result = utils.verify_notification(self.notification)
        self.assertTrue(result)

    @patch('django_bouncy.utils.grab_keyfile')
    def test_verify_subscription_notification(self, mock):
        """Test the verification of a valid subscription notification"""
        mock.return_value = self.pemfile

        notification = loader('subscriptionconfirmation')
        result = utils.verify_notification(notification)
        self.assertTrue(result)

    @patch('django_bouncy.utils.grab_keyfile')
    def test_notification_verification_failure(self, mock):
        """Test the failure of an invalid notification"""
        mock.return_value = self.pemfile
        notification = loader('bounce_notification')
        notification['TopicArn'] = 'BadArn'
        result = utils.verify_notification(notification)

        self.assertFalse(result)

    @patch('django_bouncy.utils.grab_keyfile')
    def test_subscription_verification_failure(self, mock):
        """Test the failure of an invalid subscription notification"""
        mock.return_value = self.pemfile
        notification = loader('subscriptionconfirmation')
        notification['TopicArn'] = 'BadArn'
        result = utils.verify_notification(notification)

        self.assertFalse(result)


class SubscriptionApprovalTest(BouncyTestCase):
    """Test the approve_subscription function"""
    @patch('django_bouncy.utils.urlopen')
    def test_approve_subscription(self, mock):
        """Test the subscription approval mechanism"""
        responsemock = Mock()
        responsemock.read.return_value = 'Return Value'
        mock.return_value = responsemock
        notification = loader('subscriptionconfirmation')

        response = utils.approve_subscription(notification)

        mock.assert_called_with(notification['SubscribeURL'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('ascii'), 'Return Value')

    @patch('django_bouncy.utils.urlopen')
    def test_signal_sent(self, mock):
        """
        Test that the subscription signal was sent

        Based on http://stackoverflow.com/questions/3817213/
        """
        # pylint: disable=attribute-defined-outside-init, unused-variable
        responsemock = Mock()
        responsemock.read.return_value = 'Return Value'
        mock.return_value = responsemock
        notification = loader('subscriptionconfirmation')
        self.signal_count = 0

        @receiver(signals.subscription)
        def _signal_receiver(sender, **kwargs):
            """Signal Test Receiver"""
            self.signal_count += 1
            self.signal_sender = sender
            self.signal_notification = kwargs['notification']
            self.signal_result = kwargs['result']

        response = utils.approve_subscription(notification)

        self.assertEqual(response.content.decode('ascii'), 'Return Value')
        self.assertEqual(self.signal_count, 1)
        self.assertEqual(self.signal_result, 'Return Value')
        self.assertEqual(self.signal_notification, notification)

    def test_bad_url(self):
        """Test to make sure an invalid URL isn't requested by our system"""
        old_setting = getattr(settings, 'BOUNCY_SUBSCRIBE_DOMAIN_REGEX', None)
        settings.BOUNCY_SUBSCRIBE_DOMAIN_REGEX = \
            r"sns.[a-z0-9\-]+.amazonaws.com$"
        notification = loader('bounce_notification')
        notification['SubscribeURL'] = 'http://bucket.s3.amazonaws.com'
        result = utils.approve_subscription(notification)

        self.assertEqual(result.status_code, 400)
        self.assertEqual(
            result.content.decode('ascii'), 'Improper Subscription Domain')

        if old_setting is not None:
            settings.BOUNCY_SUBSCRIBE_DOMAIN_REGEX = old_setting
