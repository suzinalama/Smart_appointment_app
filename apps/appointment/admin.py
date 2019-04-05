from django.contrib import admin
from apps.appointment.models import DaySchedule,Notification,Appointment,TimeSlot,Availability,AvailableTime

# Register your models here.


class TimeSlotInline(admin.TabularInline):
    model=Availability.time_slot.through #shows available time too



#admin.site.register(DaySchedule)
admin.site.register(Notification)
admin.site.register(Appointment)
#admin.site.register(TimeSlot)


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    inlines=[TimeSlotInline]
    list_display=['doctor','date']


#admin.site.register(AvailableTime)

