from django.db import models
from apps.user_profile.models import Doctor,User
from apps.hospital.models import Hospital


# Create your models here.

class DaySchedule(models.Model):
	MONDAY =1
	TUESDAY= 2
	WEDNESDAY=3
	THURSDAY=4
	FRIDAY=5
	SATURDAY=6
	SUNDAY=7
	
	DAYS=(
 		(MONDAY, "Monday"),
 		(TUESDAY,"Tuesday"),
 		(WEDNESDAY,"Wednesday"),
 		(THURSDAY,"Tursday"),
 		(FRIDAY,"Friday"),
 		(SATURDAY,"Saturday"),
 		(SUNDAY,"Sunday"),
 	)
	doctor=models.ForeignKey(User,on_delete=models.CASCADE)
	hospital=models.ForeignKey(Hospital, on_delete=models.CASCADE)
	day=models.PositiveSmallIntegerField(choices=DAYS)
	time_slot_from=models.TimeField()
	time_slot_to =models.TimeField()

class Notification(models.Model):
	user = models.ForeignKey(User, on_delete=None)
	message= models.TextField(max_length=1000)
	read = models.BooleanField(default=False)



