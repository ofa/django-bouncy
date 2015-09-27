"""Models for the django_bouncy app"""
from django.db import models


class Feedback(models.Model):
    """An abstract model for all SES Feedback Reports"""
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    sns_topic = models.CharField(max_length=350)
    sns_messageid = models.CharField(max_length=100)
    mail_timestamp = models.DateTimeField()
    mail_id = models.CharField(max_length=100)
    mail_from = models.EmailField()
    address = models.EmailField()
    feedback_id = models.CharField(max_length=100)
    feedback_timestamp = models.DateTimeField(verbose_name="Feedback Time")

    class Meta(object):
        """Meta info for Feedback Abstract Model"""
        abstract = True


class Bounce(Feedback):
    """A bounce report for an individual email address"""
    hard = models.BooleanField(db_index=True, verbose_name="Hard Bounce")
    bounce_type = models.CharField(
        db_index=True, max_length=50, verbose_name="Bounce Type")
    bounce_subtype = models.CharField(
        db_index=True, max_length=50, verbose_name="Bounce Subtype")
    reporting_mta = models.TextField(blank=True, null=True)
    action = models.CharField(
        db_index=True, null=True, blank=True, max_length=150,
        verbose_name="Action"
    )
    status = models.CharField(
        db_index=True, null=True, blank=True, max_length=150)
    diagnostic_code = models.TextField(null=True, blank=True, max_length=5000)

    def __unicode__(self):
        """Unicode representation of Bounce"""
        return "%s %s Bounce (message from %s)" % (
            self.address, self.bounce_type, self.mail_from)


class Complaint(Feedback):
    """A complaint report for an individual email address"""
    useragent = models.TextField(blank=True, null=True)
    feedback_type = models.CharField(
        db_index=True, blank=True, null=True, max_length=150,
        verbose_name="Complaint Type"
    )
    arrival_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        """Unicode representation of Complaint"""
        return "%s Complaint (email sender: from %s)" % (
            self.address, self.mail_from)
