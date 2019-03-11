from django.db import models
from django.utils import timezone
from apps.user_profile.models import User

#from django.conf import settings


class Admin_post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,primary_key=True)
    title = models.CharField(max_length=200)
    post = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    

    def __str__(self):
    	return self.title