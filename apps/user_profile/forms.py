from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Submit, Row, Column

User=get_user_model()



class SignUpForm(UserCreationForm):
    first_name=forms.CharField(max_length=30,required=False,help_text="Optional")
    last_name=forms.CharField(max_length=30,required=False,help_text="Optional")
    dob = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    email=forms.EmailField()
   
    
    class Meta:
        model= User
        fields = ['username','first_name','last_name','dob','email','gender','blood_groups','password1','password2']
    
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

    
     