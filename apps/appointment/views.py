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
from django.views.decorators.csrf import csrf_protect

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
        appointment=super().form_valid(form)
        notify.send(patient,recipient=user, verb="appointment created", action_object=self.object)#insert related appointment object in notification table

        #form.cleaned_data["patient"]=patient #data related only to appointment model
        #print("Clean data: ",form.cleaned_data)
        # data["patient"]=patient
        # form.cleaned_data = data
        #Appointment.objects.create(**data) # first * -> key and * -> val
        return appointment

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
    print("date:", date)
    pasrsed_date=datetime.datetime.strptime(date, "%B %d, %Y")
    doctor_id=request.GET.get("doctor")
    available=Availability.objects.get(date=pasrsed_date,doctor_id=doctor_id)
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
    if int(status) == 1 :
        verb="appointment confirmed"
    if int(status) == 2 :
        verb="appointment cancelled"

    appointment_id=request.GET.get("appointment_id")
    print(request.GET)
    print(status,appointment_id)
    update_appointment= Appointment.objects.get(id=appointment_id)
    update_appointment.status = status
    update_appointment.save()
    patient = User.objects.get(pk=update_appointment.patient.pk)
    notify.send(request.user,recipient=patient, verb=verb, action_object=update_appointment)#insert related appointment object in notification table

    print(dir(update_appointment))
    print("info>>>>>>>>>>>>>>>>>>>>>>", update_appointment.patient,update_appointment.doctor )
    doctor=Doctor.objects.get(user_id=request.user)
    
    #list of filtered appointments
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
            AvailableTime.objects.create(timeslot=timeslot, availability=availability)
        return HttpResponseRedirect(self.success_url)

def load_available_date(request):
    date_object = datetime.date.today()
    print(date_object)
    try:
        availabilities = Availability.objects.filter(date__gte=date_object).order_by("date")
    except Exception as e:
        availabilities = None
        print("something", e)

    print(availabilities)

    return render(request, "appointment/available_date.html", {"availabilities": availabilities})



@csrf_protect
def doctor_response_notification(request):
    print("here 1")
    template_name = "appointment/appointment_request_notification.html"

    slug = request.POST.get("slug")
    send_by = request.POST.get("send_by")
    notification = request.POST.get("notification")
    receiver = User.objects.get(pk=send_by)
    appointment = Appointment.objects.get(pk=notification)
    print("here 2")
    # notify.send(
    #     request.user, recipient=receiver, verb="appointment created", action_object=appointment
    # )
    return render(request, template_name, {"appointment": appointment})


def patient_response_notification(request):
    template_name = "appointment/appointment_response_notification.html"
    slug = request.POST.get("slug")
    notification = request.POST.get("notification")
    response = redirect("notifications:mark_as_read", slug=slug)
    print(response)
    appointment = Appointment.objects.get(pk=notification)
    if appointment.status == 1:
        appointment.status = "Confirmed"

    if appointment.status == 2:
        appointment.status = "Canceled"

    # notify.send(
    #     request.user, recipient=receiver, verb="appointment created", action_object=appointment
    # )
    return render(request, template_name, {"appointment": appointment})


class PrescriptionView(CreateView):
    model = Prescription
    form_class= PrescriptionForm
    prescription_table="appointment/prescription.html" 
    context_object_name="prescription"

    def get(self,request):
        context = {
			'details': Patient.objects.all()
		}
	
        return render(request, self.prescription_table,context)


    
