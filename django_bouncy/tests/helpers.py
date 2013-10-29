"""Helpful utilities for django-bouncy tests"""

import os
import json

from django.test import TestCase, RequestFactory
from django.test.utils import override_settings
from django.conf import settings

@override_settings(BOUNCY_VERIFY_CERTIFICATE=False)
class BouncyTestCase(TestCase):
    """Custom TestCase for django-bouncy"""
    @classmethod
    def setUpClass(cls):
        super(BouncyTestCase, cls).setUpClass()
        cls.old_setting = getattr(settings, 'BOUNCY_TOPIC_ARN', None)
        settings.BOUNCY_TOPIC_ARN = \
            'arn:aws:sns:us-east-1:250214102493:Demo_App_Unsubscribes'

        cls.factory = RequestFactory()
        cls.request = cls.factory.post('/')
        cls.request.META['HTTP_X_AMZ_SNS_TOPIC_ARN'] = \
            settings.BOUNCY_TOPIC_ARN

    @classmethod
    def tearDownClass(cls):
        if cls.old_setting != None:
            settings.BOUNCY_TOPIC_ARN = cls.old_setting

def loader(example_name):
    """Load examples from their JSON file and return a dictionary"""
    filename_format = '{dir}/example_{name}.json'

    dirname, _ = os.path.split(os.path.abspath(__file__))
    file_obj = open(filename_format.format(dir=dirname, name=example_name))
    return json.load(file_obj)
