from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import *
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomeUserModel
        fields = ('username', 'email', 'year_of_birth' )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# class UserChangeForm(forms.ModelForm):
#     password = ReadOnlyPasswordHashField()

#     class Meta:
#         model = CustomeUserModel
#         fields = ('email', 'password', 'year_of_birth', 'is_active', 'is_admin')

#     def clean_password(self):
#         return self.initial["password"]

# class CustomUserAdmin(BaseUserAdmin):
#     form = UserChangeForm
#     add_form = UserCreationForm
#     list_display = ('email', 'year_of_birth', 'is_admin', )
#     list_filter = ('is_admin', )
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('year_of_birth',)}),
#         ('Permissions', {'fields': ('is_admin',)}),
#         # ('Site Info', {'fields': ('year_of_birth', )}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'year_of_birth', 'password1', 'password2'),
#         }),
#     )
#     search_fields = ('email',)
#     ordering = ('email',)
#     filter_horizontal = ()

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    
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

class ActivityAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'number', 'piggy_owner', 'piggy', 'piggy_amount', ]

class ActivationKeyAdmin(admin.ModelAdmin):
    list_display = ['user', 'key', 'created_at']

class UserIdAdmin(admin.ModelAdmin):
    list_display = ['email', 'userid', 'admin_check']

admin.site.register(CustomeUserModel, CustomUserAdmin)
admin.site.register(UserBio)
admin.site.register(ProfileImage)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(MemberShip, MemberShipAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(ActivationKey, ActivationKeyAdmin)
admin.site.register(UserId, UserIdAdmin)










