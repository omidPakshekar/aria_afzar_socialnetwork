from django import forms
from .models import CustomeUserModel


class ChangeProfileImageForm(forms.ModelForm):
    class Meta:
        model = CustomeUserModel
        fields = ('profile_image',)