from django.shortcuts import render,redirect
from django.views import View
from .forms import UserAppointmentForm,PrescriptionForm,AvailabilityForm
from django.contrib import messages
from django.views.generic import CreateView,ListView,UpdateView
from apps.appointment.models import Appointment,TimeSlot,Availability,AvailableTime
from .models import Appointment,Prescription, Availability
from apps.user_profile.models import Doctor,Patient,User
from django.urls import reverse_lazy
from .models import TimeSlot
from django.db import transaction

from notifications.signals import notify
import datetime

from django.http import HttpResponse, HttpResponseRedirect


from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)

class AppointmentListView(ListView):
    model =Appointment
    template_name="appointment/appointment_list0.html"

class AppoinmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = "/user/login"

    model = Appointment
    form_class= UserAppointmentForm
    template_name="appointment/appointment_create.html"
    success_url = reverse_lazy('appointment')

    def test_func(self):
        return self.request.user.is_patient()
    
    def form_invalid(self, form):
        messages.error(self.request,"Something went wrong")
        return super().form_invalid(form)
 
 #multiple database operation
    @transaction.atomic
    def form_valid(self,form):
        available_timeslot_id = form.data.get("available_timeslot_id")
        doctor_id=form.data.get("doctor")
        print("available_timeslot_id: ",available_timeslot_id)
        available_timeslot = AvailableTime.objects.get(pk=available_timeslot_id)
        print("Timeslot ",available_timeslot.status)
        available_timeslot.status = False
        print('available_time',available_timeslot.status) #after the appoinmentment gets requested the selected timeslot status is disabled
        available_timeslot.save()
        print('user:  ', self.request.user.id)
        patient=Patient.objects.get(user=self.request.user.id)

        form.instance.patient=patient
        doctor=Doctor.objects.get(user= doctor_id)
        user=User.objects.get(pk=doctor.user.id)
        notify.send(patient,recipient=user, verb="appointment created")

        #form.cleaned_data["patient"]=patient #data related only to appointment model
        #print("Clean data: ",form.cleaned_data)
        # data["patient"]=patient
        # form.cleaned_data = data
        #Appointment.objects.create(**data) # first * -> key and * -> val
        return super().form_valid(form)

class AppointmentUpdateView(UpdateView):
    model = Appointment
    form_class= UserAppointmentForm
    success_url = reverse_lazy('appointment')

def load_doctors(request):
    department_id = request.GET.get('department')
    doctors = Doctor.objects.filter(department_id=department_id).order_by('user')
    return render(request, 'appointment/doctor_list_options.html', {'doctors': doctors})

def load_time_slots(request):
    date=request.GET.get("date")
    doctor_id=request.GET.get("doctor")
    available=Availability.objects.get(date=date,doctor_id=doctor_id)
    time_slot=available.available_time.filter(status=True)
    return render(request,"appointment/doctor_availability.html",{"time_slots":time_slot})



    # print(date, doctor_id)
    # time_slots=TimeSlot.objects.filter(
    #     available_time__availability__doctor=doctor_id,
    #     available_time__availability__date=date,
    #     available_time__status=True,

    # )
    # for i in time_slots:
    #     print(i.available_time.all())
    #     # print(dir(i.available_time))
    #     print(i.available_time.first().status,i.available_time.first().id)
       
    

    return render(request,"appointment/doctor_availability.html",{"time_slots":time_slots})

#list of the appointments 
class DoctorAppointmentListView(ListView):
    model = Appointment
    template_name="appointment/doctor_appointment.html"  
    context_object_name="appointment_list"
    login_url="/user/login"

    def test_func(self):
        return self.request.user.is_doctor()

    def get_queryset(self):
        doctor=Doctor.objects.get(user_id=self.request.user)
        
        return Appointment.objects.filter(doctor_id=doctor)
   
@transaction.atomic
def appointment_status_update(request):
    status=request.GET.get("status")
    appointment_id=request.GET.get("appointment_id")
    print(request.GET)
    print(status,appointment_id)
    update_appointment= Appointment.objects.get(id=appointment_id)
    update_appointment.status = status
    update_appointment.save()
    print(dir(update_appointment))
    print("info>>>>>>>>>>>>>>>>>>>>>>", update_appointment.patient,update_appointment.doctor )
    doctor=Doctor.objects.get(user_id=request.user)
    appointment_list= Appointment.objects.filter(doctor_id=doctor)
    
    return render(request,"appointment/doctor_appointment.html",{"appointment_list":appointment_list})

class AvailabilityCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = "/users/login/"
    permission_denied_message = "You have no permission to view this page."

    model = Availability
    form_class = AvailabilityForm
    template_name = "appointment/availability_create.html"
    success_url = reverse_lazy("appointment")

    def test_func(self):
        return self.request.user.is_doctor()

    def form_invalid(self, form):
        print(form.data)
        print(form.errors)
        messages.error(self.request, "Something went wrong.")
        return super().form_invalid(form)

    @transaction.atomic
    def form_valid(self, form):
        date = form.cleaned_data["date"]
        timeslots = form.cleaned_data["time_slot"]
        doctor = Doctor.objects.get(user=self.request.user.id)
        availability = Availability.objects.create(date=date, doctor=doctor)
        for timeslot in timeslots:
            AvailableTime.objects.create(timeslot=timeslot, availablity=availability)
        return HttpResponseRedirect(self.success_url)

def load_available_date(request):
    date_object = datetime.date.today()
    try:
        availabilities = Availablity.objects.filter(date__gte=date_object).order_by("date")
    except:
        availabilities = None

    print(availabilities)

    return render(request, "appointment/available_date.html", {"availabilities": availabilities})

class PrescriptionView(ListView):
    model = Prescription
    form_class= PrescriptionForm
    template_name="appointment/prescription.html" 
    context_object_name="prescription"

