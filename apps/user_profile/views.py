from django.shortcuts import render, redirect
from .models import User,Doctor,Patient
from apps.appointment.models import Availability,AvailableTime,Appointment
from django.views import View
from .forms import SignUpForm#,UserAppointmentForm
from django.views.generic import ListView, UpdateView,DetailView
from django.views.generic.base import RedirectView
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.http import HttpResponse, HttpResponseRedirect
from apps.appointment.models import Prescription
from django.shortcuts import get_object_or_404


class UserLoginView(View):
    login_template="user_profile/login.html"
    def get(self,request):
        return render(request, self.login_template)

class UserSignUp(View):
    signup_template = "user_profile/signup.html"
    def get(self, request):
        form = SignUpForm()
        return render(request, self.signup_template, {"form": form})

    def post(self, request):
        signup_template = "user_profile/signup.html"
        print("abccc")
        if request.method == "POST":
            form = SignUpForm(request.POST)
            print("donee",form.errors)
            if form.is_valid():
                print("inside if")
                user = form.save(commit=False)
                user.is_active = False
                user.role = 1 # Patient role is one
            
                user.save()
                Patient.objects.create(user=user)

                current_site = get_current_site(request)
                subject = "Activate Your Appointment APP Account"
                message = render_to_string(
                    "user_profile/account_activation_email.html",
                    {
                        "user": user,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        # "uid": urlsafe_base64_encode(force_bytes(user.pk)).decode(),

                        "token": PasswordResetTokenGenerator().make_token(user),
                    },
                )
                print("ABC")
                user.email_user(subject, message)
                print("ABC2")
                return render(request, signup_template)
            else:
                return render(request, self.signup_template, {"form": form})

            
      
        else:
            form = SignUpForm()
            return render(request, self.signup_template, {"form": form})


class UserAccountActivationSent(RedirectView):
    url = "/user/login"


def user_activate(request, uidb64, token):
    print(uidb64, token)
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and PasswordResetTokenGenerator().check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("account_activation_sent")
    return render(request, 'user_profile/account_activation_invalid.html')


# @login_required
# def account(request):
# 	return render(request,'user_profile/account.html')

class ReportListView(ListView):
    model = Prescription
    template_name="user_profile/patient_report.html"  
    context_object_name="report_list"
    login_url="/user/login"

    def test_func(self):
        return self.request.user.is_patient()

    def get_queryset(self):
        patient=Patient.objects.get(user_id=self.request.user)
        return Prescription.objects.filter(patient_id = patient )


class UserReportDetailView(DetailView):
    model = Prescription
    template_name="user_profile/report_detail.html"
    context_object_name="report"

    
    def get(self,request,*args,**kwargs):
        report = get_object_or_404(Prescription,pk=kwargs['pk'])
        print("Report: ",report)
        return render(request, self.template_name, {'report': report} )



class UserInfoView(View):
    info_template="user_profile/info.html"
    def get(self,request):
        return render(request, self.info_template)


class InfoEditView(View):
    model = User
    template_name="user_profile/info.html"
    context_object_name="edit"
    login_url="/user/login"

    def get(self,request,*args,**kwargs):
        edit = get_object_or_404(User,pk=kwargs['pk'])
        print("User: ", edit)
        return render(request, self.template_name, {'edit': edit} )


class DoctorsListView(ListView):
    model=Doctor
    paginate_by=10
    template_name="user_profile/search.html"
    
    def get(self,request):
        context = {
            'doctors': Doctor.objects.all()
        }
        
        return render(request, self.template_name,context)


class DoctorSearchListView(ListView):
    model=Doctor
    paginate_by=10
    template_name="user_profile/search.html"
    context_object_name="searches"
    
    # def get(self,request):
    #     context = {
    #         'doctors': Doctor.objects.all()
    #     }
        
    #     return render(request, self.template_name,context)

    def get_queryset(self):
        keywords=self.request.GET.get("q")
        qs = Doctor.objects.all() if keywords else Doctor.objects.none()

        if keywords:
            query= SearchQuery(keywords)
            name_vector=SearchVector("user__username",weight="A")
            department_vector=SearchVector("department__department_name",weight="B")
            firstname_vector=SearchVector("user__first_name",weight="C")
            lastname_vector=SearchVector("user__last_name",weight="D")
            vectors=name_vector + department_vector + firstname_vector + lastname_vector
            qs=qs.annotate(search=vectors).filter(search=query)
            qs=qs.annotate(rank=SearchRank(vectors,query)).order_by("education")

        return qs






   