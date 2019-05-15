from django.contrib import admin
from apps.payment.models import Payment


# admin.site.register(Payment)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display=['patient','status',]
