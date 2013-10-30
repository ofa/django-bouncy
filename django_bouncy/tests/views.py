"""Tests for views.py in the django-bouncy app"""
# pylint: disable=protected-access

import json

from django.test import RequestFactory
from django.test.utils import override_settings

from django_bouncy.tests.helpers import BouncyTestCase, loader
from django_bouncy.views import endpoint


class BouncyEndpointViewTest(BouncyTestCase):
    """Test the endpoint view"""
    def setUp(self):
        """Setup the test"""
        self.factory = RequestFactory()
        self.request = self.factory.post('/')
        self.request.META['HTTP_X_AMZ_SNS_TOPIC_ARN'] = \
            settings.BOUNCY_TOPIC_ARN

    def test_success(self):
        """Test a successful request"""
        self.request._body = json.dumps(self.notification)
        result = endpoint(self.request)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content, 'Bounce Processed')

    @override_settings(BOUNCY_TOPIC_ARN='Bad ARN')
    def test_bad_topic(self):
        """Test the response if the topic does not match the settings"""
        self.request._body = json.dumps(self.notification)
        result = endpoint(self.request)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.content, 'Bad Topic')

    def test_no_header(self):
        """Test the results if the request does not have a topic header"""
        request = self.factory.post('/')
        request._body = json.dumps(self.notification)
        result = endpoint(request)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.content, 'No TopicArn Header')

    def test_invalid_json(self):
        """Test if the notification does not have a JSON body"""
        self.request._body = "This Is Not JSON"
        result = endpoint(self.request)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.content, 'Not Valid JSON')

    def test_missing_necessary_key(self):
        """Test if the notification is missing vital keys"""
        self.request._body = json.dumps({})
        result = endpoint(self.request)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.content, 'Request Missing Necessary Keys')

    def test_unknown_notification_type(self):
        """Test an unknown notification type"""
        notification = loader('bounce_notification')
        notification['Type'] = 'NotAKnownType'
        self.request._body = json.dumps(notification)
        result = endpoint(self.request)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.content, 'Unknown Notification Type')

    def test_bad_certificate_url(self):
        """Test an unknown certificate hostname"""
        notification = loader('bounce_notification')
        notification['SigningCertURL'] = 'https://baddomain.com/cert.pem'
        self.request._body = json.dumps(notification)
        result = endpoint(self.request)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.content, 'Improper Certificate Location')


