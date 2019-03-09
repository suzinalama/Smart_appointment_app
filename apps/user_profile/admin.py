from django.contrib import admin
from apps.user_profile.models import User,Doctor,Patient,Contact
# Register your models here.

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name=='user':
            kwargs['queryset'] = User.objects.filter(role=2)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    list_display=['user','department','time_slot','education']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=['username','first_name','last_name','email','gender','dob','blood_groups']
# admin.site.register(User)

#admin.site.register(Doctor,DoctorAdmin)
admin.site.register(Contact)

admin.site.register(Patient)
