from rest_framework import serializers

from ..models import Payment

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ( 'created_date', 'amount', 'payment_system')











