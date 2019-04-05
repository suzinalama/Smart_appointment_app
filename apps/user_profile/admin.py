from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.user_profile.models import User,Doctor,Patient,Contact,Prescription,Bill
from apps.hospital.models import Department,Hospital

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.user_profile.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
User=get_user_model()

class ContactInline(admin.TabularInline):
    model = Contact


   

def upper_case_name(obj):
    return ("%s %s" % (obj.first_name, obj.last_name)).upper()
upper_case_name.short_description = 'Name'

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name =='user':
            kwargs['queryset'] = User.objects.filter(role=1)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    list_display=['user','height','weight']
    



@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name=='user':
            kwargs['queryset'] = User.objects.filter(role=2)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    list_display=['user','department','education']
    
    
class CustomUserAdmin(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username',upper_case_name,'gender','email', 'dob')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name','email','dob','gender','profile_pic')}),
        ('Permissions', {'fields': ('role','is_active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','password1','password2')}
         ),
    )

    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()
    inlines = [
                 ContactInline,
            ]



admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)

# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
  
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = User

    
#     list_display=('username',upper_case_name,'email','gender','dob','blood_groups')
#     inlines = [
#                  ContactInline,
#             ]
    
    
    
#admin.site.register(User, CustomUserAdmin)
    


    
    #exclude=['last_login']
# admin.site.register(User)

#admin.site.register(Doctor,DoctorAdmin)
admin.site.register(Contact)
# admin.site.register(Prescription)
# admin.site.register(PayBill)

