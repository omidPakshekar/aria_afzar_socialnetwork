from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(PaymentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Payment
        fields = ["amount", "payment_system"]


class ChangePaymentStatusForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['status', 'description']
