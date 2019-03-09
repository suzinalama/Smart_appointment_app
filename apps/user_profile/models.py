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

	def __str__(self):
		return self.username

class Contact(models.Model):
 	user=models.ForeignKey(User, on_delete = models.CASCADE, related_name="contacts")
 	contact_no = PhoneField(blank=True, help_text='Contact phone number', unique=True)
	 

 	def __str__(self):
 		return self.contact_no



class Doctor(models.Model):
 	user=models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
 	department=models.ForeignKey(Department,on_delete=models.CASCADE)
 	education =models.CharField(max_length=500)
 	time_slot=models.DurationField()

 	def __str__(self):
 		return self.user.username

class Patient(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
	height=models.PositiveIntegerField()
	weight=models.PositiveIntegerField()
	
	def __str__(self):
 		return self.user




  

