"""Tests for utils.py in the django-bouncy app"""

from mock import Mock, patch

from django_bouncy.tests.helpers import BouncyTestCase, loader
from django_bouncy import utils

class TestVerificationSystem(BouncyTestCase):
    """Test the message verification utilities"""
    @patch('django_bouncy.utils.urllib2.urlopen')
    def test_grab_keyfile(self, mock):
        """Test the grab_keyfile plugin"""
        responsemock = Mock()
        responsemock.read.return_value = self.pemfile
        mock.return_value = responsemock
        result = utils.grab_keyfile('http://www.fakeurl.com')

        mock.assert_called_with('http://www.fakeurl.com')
        self.assertEqual(result, self.pemfile)

    @patch('django_bouncy.utils.urllib2.urlopen')
    def test_bad_keyfile(self, mock):
        """Test a non-valid keyfile"""
        responsemock = Mock()
        responsemock.read.return_value = 'Not A Certificate'
        mock.return_value = responsemock

        with self.assertRaises(ValueError) as context_manager:
            utils.grab_keyfile('http://www.fakeurl.com')

        the_exception = context_manager.exception
        self.assertEqual(the_exception[0], 'Invalid Certificate File')

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
