from django.urls import reverse
from django.conf import settings
from apps.appointment.models import Appointment
from paypal.standard.forms import PayPalPaymentsForm
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from apps.user_profile.models import Patient
from django.shortcuts import render, redirect
from .forms import CheckoutForm

def process_payment(request):
    user = request.user
    print("patient id", user.id)
    patient = get_object_or_404(Patient, user=user.id)
    print("patient: ", patient)
    appointment = get_object_or_404(Appointment, id=15, patient=patient)
    print("HERE:::")
    host = request.get_host()

    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": 100,
        "item_name": "Order {}".format(appointment.id),
        "invoice": str(appointment.id),
        "notify_url": "http://{}{}".format(host, reverse("paypal-ipn")),
        "return_url": "http://{}{}".format(host, reverse("payment_done")),
        "cancel_return": "http://{}{}".format(host, reverse("payment_cancelled")),
    }

    print("form>>>>>>>>>>>")
    form = PayPalPaymentsForm(initial=paypal_dict)
    print("form============")
    return render(
        request, "payment/process_payment.html", {"appointment": appointment, "form": form}
    )


def payment_done(request):
    return render(request, "payment/payment_done.html")


def payment_canceled(request):
    return render(request, "payment/payment_cancelled.html")

def checkout(request, id):
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            return redirect("process_payment")
    else:
        form = CheckoutForm()
        return render(request, "payment/checkout.html", {"form": form})