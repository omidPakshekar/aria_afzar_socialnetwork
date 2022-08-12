from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import *

class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = () 
    fieldsets= ()

class UserInline(admin.StackedInline):
    model = CustomeUserModel

class WalletAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'amount', 'wallet_key']

class MemberShipAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'month', 'amount', 'started_date', 'expired_day']


admin.site.register(CustomeUserModel, CustomUserAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(MemberShip, MemberShipAdmin)
