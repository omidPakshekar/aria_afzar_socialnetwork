from django.contrib import admin

from .models import *


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'payment_system', 'amount', 'created_date']

class PiggyBankAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'started_time', 'finish_time', 'day_left', 'long']


admin.site.register(Payment, PaymentAdmin)
admin.site.register(PiggyBank, PiggyBankAdmin)

