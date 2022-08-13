from django.contrib import admin

from .models import *


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'payment_system', 'amount', 'created_date']

class PiggyBankAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'started_time', 'expired_day']


admin.site.register(Payment, PaymentAdmin)
admin.site.register(PiggyBank, PiggyBankAdmin)

