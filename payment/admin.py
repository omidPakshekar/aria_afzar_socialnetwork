from django.contrib import admin

from .models import *


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'created_date', 'created_time']

class PiggyBankAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'started_time', 'expired_day']


admin.site.register(Payment, PaymentAdmin)
admin.site.register(PiggyBank, PiggyBankAdmin)

