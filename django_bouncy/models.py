"""Models for the django_bouncy app"""
from django.db import models

class Feedback(models.Model):
    """An abstract model for all SES Feedback Reports"""
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    sns_topic = models.CharField(db_index=True, max_length=350)
    sns_messageid = models.CharField(max_length=100)
    mail_timestamp = models.DateTimeField()
    mail_id = models.CharField(max_length=100)
    mail_from = models.EmailField()
    address = models.EmailField()
    feedback_id = models.CharField(max_length=100)
    feedback_timestamp = models.DateTimeField()

    class Meta(object):
        """Meta info for Feedback Abstract Model"""
        abstract = True


class Bounce(Feedback):
    """A bounce report for an individual email address"""
    hard = models.BooleanField(db_index=True)
    bounce_type = models.CharField(db_index=True, max_length=50)
    bounce_subtype = models.CharField(db_index=True, max_length=50)
    reporting_mta = models.TextField(blank=True, null=True)
    action = models.CharField(
        db_index=True, null=True, blank=True, max_length=150)
    status = models.CharField(
        db_index=True, null=True, blank=True, max_length=150)
    diagnostic_code = models.CharField(null=True, blank=True, max_length=150)


class Complaint(Feedback):
    """A complaint report for an individual email address"""
    useragent = models.TextField(blank=True, null=True)
    feedback_type = models.CharField(
        db_index=True, blank=True, null=True, max_length=150)
    arrival_date = models.DateTimeField(blank=True, null=True)
