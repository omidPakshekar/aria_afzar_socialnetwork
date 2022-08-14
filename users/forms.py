from django import forms
from .models import CustomeUserModel
from payment.forms import PaymentForm

class ChangeProfileImageForm(forms.ModelForm):
    class Meta:
        model = CustomeUserModel
        fields = ('profile_image',)

