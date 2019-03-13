from django.contrib import admin

from apps.post.models import Admin_post
from apps.user_profile.models import User,Admin

@admin.register(Admin_post)
class PostAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name=='user':
            kwargs['queryset'] = User.objects.filter(role=4)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    