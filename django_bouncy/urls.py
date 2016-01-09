"""URLs for the Django-Bouncy App"""
from django.conf.urls import url
# pylint: disable=invalid-name
from django_bouncy.views import endpoint

urlpatterns = [
    url(r'^$', endpoint)
]
