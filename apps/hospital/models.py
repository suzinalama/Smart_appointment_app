from django.db import models
from django.conf import settings

class Department(models.Model):
 	department_name =models.CharField(max_length=50, unique=True)

 	def __str__(self):
 		return self.department_name

class Hospital(models.Model):
	user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,primary_key=True)
	hospital_name=models.CharField(max_length=100)
	no_of_beds=models.IntegerField()
	latitude=models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
	longitude=models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
	departments=models.ManyToManyField(Department)
	
	def __str__(self):
 		return self.hospital_name


