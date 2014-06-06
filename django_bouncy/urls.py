"""URLs for the Django-Bouncy App"""
# pylint: disable=invalid-name
from django.conf.urls import patterns

from django_bouncy.views import endpoint

urlpatterns = patterns(
    '',
    (r'^$', endpoint)
)
