from django.urls import path,re_path
from apps.appointment import views

urlpatterns = [
    path('', views.AppointmentListView.as_view(), name='appointment'),
    path('add/', views.AppoinmentCreateView.as_view(), name='appointment-add'),
    path('<int:pk>/', views.AppointmentUpdateView.as_view(), name='appointment_change'),
    path('ajax/load-doctors/', views.load_doctors, name='ajax_load_doctors'),  
    path('ajax/load-time-slots/', views.load_time_slots, name='ajax_load_timeslots'),
    path('ajax/update-appointment-status/', views.appointment_status_update, name='update-appointment-status'),
    path('appoint', views.DoctorAppointmentListView.as_view(), name ='appoint'),
    path('prescription', views.PrescriptionView.as_view(), name ='prescription'),
    path('prescription_detail/<int:pk>/', views.PrescriptionDetailView.as_view(), name='prescription_detail'),
    path("create-availability", views.AvailabilityCreateView.as_view(), name="create-availability"),

    path(
        "ajax/load-available-date/", views.load_available_date, name="ajax_load_available_date"
    ), 
    path("read-notification/doctor/",
    views.doctor_response_notification,
    name="doctor-response-notification",
    ),
    path("read-notification/patient/",
    views.patient_response_notification,
    name="patient-response-notification",
    ),


  

    #path('appointment',UserAppointmentView.as_view(), name ='appointment'),

]