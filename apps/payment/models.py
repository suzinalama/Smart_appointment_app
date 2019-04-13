from django.db import models
from apps.appointment.models import Appointment
from apps.user_profile.models import User



class Payment(models.Model):
    appointment= models.OneToOneField(Appointment,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    patient=models.ForeignKey(User,on_delete=models.CASCADE)

