from django import forms
from .models import Payment


class CartForm(forms.Form):
    appointment_id = forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(CartForm, self).__init__(*args, **kwargs)


class CheckoutForm(forms.ModelForm):
    appointment_fee = forms.CharField(
    widget=forms.TextInput(attrs={"readonly": "readonly", "value": 500})
    )

    class Meta:
        model = Payment
        exclude = ("bill", "appointment", "patient", "status")
