from django.db import models
from django.db.models.signals import post_save

from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from apps.hospital.models import Department
from phone_field import PhoneField





class User(AbstractUser):
	PATIENT=1
	DOCTOR=2
	HOSPITAL=3
	ADMIN=4
	ROLE_CHOICES =(
  		(PATIENT, "Patient"),
  		(DOCTOR, "Doctor"),
  		(HOSPITAL, "Hospital"),
  		(ADMIN,"Admin"),
  	)
	
	GENDER_CHOICES=(("M","Male"),("F","Female"),("O","Other"))
	BLOOD_GROUPS=(("A+","A+ve"),("B+","B+ve"),("A-","A-ve"),("B-","B-ve"),("O+","O+ve"),("O+","O-ve"))
	role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES,null=True,blank=True)
	gender = models.CharField(max_length=1,choices=GENDER_CHOICES,null=True,blank=True)
	dob = models.DateField(null=True,blank=True)
	blood_groups=models.CharField(max_length=2,choices=BLOOD_GROUPS)
	profile_pic = models.ImageField(default='default.png', upload_to='profile_pic',null=True,blank=True)
	password=models.CharField(('password'),max_length=128,unique=True)
	

	def __str__(self):
		return self.username
	
	def is_doctor(self):
		return self.role ==self.DOCTOR
	
	def is_patient(self):
		return self.role ==self.PATIENT
	
	class Meta:
		verbose_name_plural ="Users"
	
	
	
class Contact(models.Model):
	user=models.ForeignKey(User, on_delete = models.CASCADE, related_name="contacts")
	contact_no = PhoneField(blank=True, help_text='Contact phone number')
	


class Doctor(models.Model):
 	user=models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
 	department=models.ForeignKey(Department,on_delete=models.CASCADE)
 	education =models.CharField(max_length=500)
 

 	def __str__(self):
 		return f'{self.user.username} Doctor'
	

	
class Patient(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
	height=models.PositiveIntegerField(null=True)
	weight=models.PositiveIntegerField(null=True)
	
	def __str__(self):
 		return f'{self.user.username} Patient'

class Admin(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
		
	def __str__(self):
 		return f'{self.user.username} Admin'



class Prescription(models.Model):
	date=models.DateField()
	description = models.TextField()
	#appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE,primary_key=True)
	

	def __str__(self):
		return f"Date: {self.date}"
	
	
class Bill(models.Model):

	patient= models.OneToOneField(Patient, on_delete=models.CASCADE, primary_key=True)
	staff_id = models.ForeignKey(Admin,on_delete=models.CASCADE)
	bill_status=models.BooleanField(default=False)

	def __str__(self):
		return f"amount: {self.amount}"
	


  

