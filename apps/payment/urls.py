from django.urls import path, re_path
from . import views

urlpatterns = [
path("checkout/<int:id>", views.checkout, name="checkout"),
path("process-payment/", views.process_payment, name="process_payment"),
path("payment-done/", views.payment_done, name="payment_done"),
path(
"payment-cancelled/", views.payment_canceled, name="payment_cancelled"
), # <-- this one here
]