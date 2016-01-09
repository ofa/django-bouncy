"""Admin code for django_bouncy app"""

from django.contrib import admin

from django_bouncy.models import Bounce, Complaint, Delivery


class BounceAdmin(admin.ModelAdmin):
    """Admin model for 'Bounce' objects"""
    list_display = (
        'address', 'mail_from', 'bounce_type', 'bounce_subtype', 'status')
    list_filter = (
        'hard', 'action', 'bounce_type', 'bounce_subtype',
        'feedback_timestamp'
    )


class ComplaintAdmin(admin.ModelAdmin):
    """Admin model for 'Complaint' objects"""
    list_display = ('address', 'mail_from', 'feedback_type')
    list_filter = ('feedback_type', 'feedback_timestamp')


class DeliveryAdmin(admin.ModelAdmin):
    """Admin model for 'Delivery' objects"""
    list_display = ('address', 'mail_from')
    list_filter = ('feedback_timestamp',)


admin.site.register(Bounce, BounceAdmin)
admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Delivery, DeliveryAdmin)
