from django.contrib import admin

from .models import *


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'payment_system', 'amount', 'created_date']

class PiggyBankAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'started_time', 'finish_time', 'day_left', 'long']

class TransactionHistoryAdmin(admin.ModelAdmin):
    list_display = ['owner', 'id', 'amount', 'kind', 'created_time']


admin.site.register(Payment, PaymentAdmin)
admin.site.register(PiggyBank, PiggyBankAdmin)
admin.site.register(TransactionHistory, TransactionHistoryAdmin)
