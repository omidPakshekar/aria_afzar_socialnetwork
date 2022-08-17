from rest_framework import serializers

from ..models import Payment
from users.models import CustomeUserModel, Wallet

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

    def update(self, instance, validated_data):
        print('serializer', validated_data)
        # transaction are accept --> add amount to wallet
        if validated_data['status'] == 'Accept' and not instance.done:
            instance.done = True
            wallet_ = Wallet.objects.get(owner=instance.user)
            wallet_.amount = wallet_.amount + instance.amount
            wallet_.save()  
        return super().update(instance, validated_data)





