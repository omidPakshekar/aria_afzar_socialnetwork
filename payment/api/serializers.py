from rest_framework import serializers

from ..models import Payment
from users.models import CustomeUserModel

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (  'amount', 'payment_system')

class UserInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomeUserModel
        fields = ['id', 'username']

class PaymentListSerializer(serializers.ModelSerializer):
    user = UserInlineSerializer()
    class Meta:
        model = Payment
        fields = "__all__"


class PaymentChangeStatus(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'status', 'description']






