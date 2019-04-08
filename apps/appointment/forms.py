from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Appointment,Prescription,Availability,TimeSlot
from apps.user_profile.models import Doctor
from django.forms.fields import DateField

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .widgets import DatePickerInput
import datetime

User=get_user_model()

class UserAppointmentForm(forms.ModelForm):
    appointment_date = forms.DateField()
    

    class Meta:
        model= Appointment
        fields = ['appointment_date','department','doctor']

    
     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.none()

        #data changed from AJAX 
        if "department" in self.data:
            try:
                department_id =int(self.data.get("department"))
                self.fields["doctor"].queryset=Doctor.objects.filter(
                    department=department_id
                ).order_by("user")
            except (ValueError,TypeError):
                pass
        if "appointment_date" in self.data:
            self.fields["appointment_date"].input_formats=["%B %d, %Y"]
    
    def clean_appointment_date(self):
        data = self.cleaned_data.get('appointment_date')
        
        # Checking if a date is not in the past. 
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - appointment_date in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        # if data > datetime.date.today() + datetime.timedelta(weeks=1):
        #     raise ValidationError(_('Invalid date - renewal more than 1 weeks ahead'))

        # to always return the cleaned data
        return data

class AvailabilityForm(forms.ModelForm):
    # time_slot = forms.ModelMultipleChoiceField()
    time_slot = forms.ModelMultipleChoiceField(
        queryset=TimeSlot.objects.all(), widget=forms.CheckboxSelectMultiple, required=True
    )

    class Meta:
        model = Availability
        fields = ("date", "time_slot")
        widgets = {"date": forms.DateInput(attrs={"class": "datepicker", "id": "datepicker"})}


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model= Prescription
        fields = ('prescription',)
        


	

