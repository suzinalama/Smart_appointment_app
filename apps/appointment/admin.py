from django.contrib import admin
from apps.appointment.models import DaySchedule,Notification
# Register your models here.
admin.site.register(DaySchedule)
admin.site.register(Notification)