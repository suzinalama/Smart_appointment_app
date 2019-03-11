
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.index, name ='app-index'),
#     path('about/', views.about, name ='app-about'),
#     path('services/', views.services, name ='app-services'),
#     path('contact/', views.contact, name ='app-contact'),
#     path('book/', views.contact, name ='app-book'),
#     path('billPayment/', views.contact, name ='app-billPay'),
#     path('findDoctor/', views.contact, name ='app-findDoc'),
   
# ]

from django.urls import path
from . import views
from .views import UserIndexView,UserAboutView,UserContactView,UserServicesView

urlpatterns = [
    path('index', UserIndexView.as_view(), name ='app-index'),
    path('about', UserAboutView.as_view(), name ='app-about'),
    path('services', UserServicesView.as_view(), name ='app-services'),
    path('contact', UserContactView.as_view(), name ='app-contact'),
    # path('book/', views.contact, name ='app-book'),
    # path('billPayment/', views.contact, name ='app-billPay'),
    # path('findDoctor/', views.contact, name ='app-findDoc'),
   
   
]