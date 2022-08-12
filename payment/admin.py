from django.contrib import admin

from .models import Payment, PiggyBank


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'created_date', 'created_time']

admin.site.register(Payment, PaymentAdmin)
admin.site.register(PiggyBank)
