from django.contrib import admin
from apps.hospital.models import Department,Hospital
# Register your models here.
admin.site.register(Department)
admin.site.register(Hospital)