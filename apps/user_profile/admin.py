from django.contrib import admin
from apps.user_profile.models import User,Doctor,Patient,Contact
from apps.hospital.models import Department,Hospital


class ContactInline(admin.TabularInline):
    model = Contact


   

def upper_case_name(obj):
    return ("%s %s" % (obj.first_name, obj.last_name)).upper()
upper_case_name.short_description = 'Name'

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name=='user':
            kwargs['queryset'] = User.objects.filter(role=1)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    list_display=['user','height','weight']
    
    

    



@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name=='user':
            kwargs['queryset'] = User.objects.filter(role=2)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    list_display=['user','department','time_slot','education']
    
    
    

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    
    list_display=('username',upper_case_name,'email','gender','dob','blood_groups')
    inlines = [
                 ContactInline,
            ]
            
    exclude =['groups','is_superuser','last_login','user_permissions']


    
    #exclude=['last_login']
# admin.site.register(User)

#admin.site.register(Doctor,DoctorAdmin)
admin.site.register(Contact)


