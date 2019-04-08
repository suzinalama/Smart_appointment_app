from django.db import models
from apps.user_profile.models import Doctor,User,Patient
from apps.hospital.models import Hospital,Department




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
	note=models.CharField(max_length=1000,blank=True)
	day=models.PositiveSmallIntegerField(choices=DAYS)
	time_slot_from=models.TimeField()
	time_slot_to =models.TimeField()



	
class TimeSlot(models.Model):
	available_from=models.TimeField("Appointment time slot")
	available_to=models.TimeField("Appointment time ends")

	def __str__(self):
		return f"Start time: {self.available_from} End time: {self.available_to}"


class Availability(models.Model):
	date=models.DateField()
	doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
	time_slot=models.ManyToManyField(TimeSlot,through="AvailableTime",related_name="available")

	def __str__(self):
		return f"Date: {self.date}"

	class Meta:
		verbose_name_plural="availabilities"

class AvailableTime(models.Model):
	timeslot=models.ForeignKey(TimeSlot,on_delete=models.CASCADE,related_name="available_time")
	availability = models.ForeignKey(
		Availability, on_delete=models.CASCADE,related_name="available_time"
	)
	status=models.BooleanField(default=True)



class Notification(models.Model):
	user = models.ForeignKey(User, on_delete=None)
	message= models.TextField(max_length=1000)
	read = models.BooleanField(default=False)

class Appointment(models.Model):
	
	CONFIRMED = 1
	CANCELLED = 2
	WAITING = 3
	STATUS_CODES = ((CONFIRMED, "Confirmed"), (CANCELLED, "Cancelled"), (WAITING, "Waiting"))
	appointment_date = models.DateField()
	#appointment_date = models.OneToOneField(Availability, on_delete=models.CASCADE )
	status = models.PositiveSmallIntegerField(choices=STATUS_CODES,default=WAITING)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	department = models.ForeignKey(Department, on_delete=models.CASCADE)
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	timeslot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE,null=True)


class Prescription(models.Model):
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	appointment_date=models.DateField()
	prescription=models.CharField(max_length=1000)
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
     
	def __str__(self):
		return f"appointment_date: {self.appointment_date}"
	




