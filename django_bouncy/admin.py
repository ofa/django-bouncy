"""Admin code for django_bouncy app"""

from django.contrib import admin

from django_bouncy.models import Bounce, Complaint

admin.site.register(Bounce)
admin.site.register(Complaint)
