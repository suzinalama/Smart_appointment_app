from django import forms
from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from apps.user_profile.models import User
from django.contrib.admin.widgets import AdminDateWidget
from apps.user_profile.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
import datetime

class UserCreationForm(forms.ModelForm):
  
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        fields = ('email','dob',)
        model= User

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords dont match')
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email','password','dob','is_active')

    def clean_password(self):
        return self.initial['password']
# class CustomUserCreationForm(UserCreationForm):

#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields =  ('username','first_name','last_name','email','gender','dob','blood_groups')
        

# class CustomUserChangeForm(UserChangeForm):

#     class Meta:
#         model = User
#         fields = ('username','first_name','last_name','email','gender','dob','blood_groups')
       


class SignUpForm(UserCreationForm):
    first_name=forms.CharField(max_length=30,required=False,help_text="Optional")
    last_name=forms.CharField(max_length=30,required=False,help_text="Optional")
    dob = forms.DateField()
 
    
    email=forms.EmailField()
   
    
    class Meta:
        model= User
      
        fields = ['username','first_name','last_name','dob','email','gender','blood_groups','password1','password2', ]

    
    def clean_email(self):
        
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')

