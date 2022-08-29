from django import forms
from .models import CustomeUserModel, MemberShip
from payment.forms import PaymentForm

# class ChangeProfileImageForm(forms.ModelForm):
#     class Meta:
#         model = CustomeUserModel
#         fields = ('profile_image',)

class MemberShipCreateForm(forms.ModelForm):
    class Meta:
        model = MemberShip
        fields = ['month', ]



        