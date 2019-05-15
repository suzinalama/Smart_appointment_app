from django.urls import path,re_path
from django.contrib.auth import views
from .views import UserAccountActivationSent, UserSignUp,user_activate,DoctorSearchListView,UserInfoView,ReportListView,UserReportDetailView,InfoEditView,DoctorsListView #,InfoEditView



urlpatterns = [
    path('login', views.LoginView.as_view(template_name="user_profile/login.html"), name ='login'),
    path('logout', views.LogoutView.as_view(template_name="user_profile/logout.html"), name ='logout'),
    path('patient-report', ReportListView.as_view(), name ='patient-report'),
    path('report_detail/<int:pk>/', UserReportDetailView.as_view(), name ='report_detail'),
    path('register', UserSignUp.as_view(), name ='register'),
    path('search',  DoctorSearchListView.as_view(), name ='search'),
    path('doctor',  DoctorsListView.as_view(), name ='doctor'),

    path('info',  UserInfoView.as_view(), name ='info'),
    path('info_edit/<int:pk>/', InfoEditView.as_view(), name ='info_edit'),

    path(
        'password-reset', 
        views.PasswordResetView.as_view(
            template_name="user_profile/password_reset_form.html",
            email_template_name="user_profile/password_reset_email.html"),
            name ='password-reset'),
    path("password-reset/done",views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(
            template_name="user_profile/password_reset_confirmation_form.html", success_url="/home/index"
        ),
        name="password_reset_confirm",
    ),
    path("reset/done/", views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("account-activation-sent", UserAccountActivationSent.as_view(), name="account_activation_sent"),
    re_path(r'^account-activation/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', user_activate, name="account-activation"),

    
]