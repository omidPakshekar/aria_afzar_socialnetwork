from rest_framework import serializers

from users.api.serializers import ImageInlineSerializer, UserIdInlineSerializer

from ..models import Payment, TransactionHistory
from users.models import CustomeUserModel, Wallet

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (  'amount', 'payment_system')

class UserInlineSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField(source='profile_pic', read_only=True)
    class Meta:
        model = CustomeUserModel
        fields = ['id', 'username', 'name', 'userid', 'profile_pic']
    def get_profile_pic(self, obj):
        if obj.profile_pic.admin_check == False or self.context['request'].user.is_anonymous:
            return self.context['request'].build_absolute_uri('/media/default_image.jpg')
        return ImageInlineSerializer(instance=obj.profile_pic, context={'request' : self.context['request']}).data
class UserInlineSerializerNonAdmin(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField(source='profile_pic', read_only=True)
    userid      = serializers.SerializerMethodField()
    class Meta:
        model = CustomeUserModel
        fields = ['id', 'username', 'name', 'userid', 'profile_pic']
    def get_profile_pic(self, obj):
        if obj.profile_pic.admin_check == False or self.context['request'].user.is_anonymous:
            return self.context['request'].build_absolute_uri('/media/default_image.jpg')
        return ImageInlineSerializer(instance=obj.profile_pic, context={'request' : self.context['request']}).data['image']
    def get_userid(self, obj):
        if  obj.userid == None:
            return None 
        if obj.userid.admin_check == False and not self.request.user.is_admin:
            return None
        return UserIdInlineSerializer(instance=obj.userid).data['userid']

    
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


class TransactionHistorySerializer(serializers.ModelSerializer):
    owner = UserInlineSerializer()
    class Meta:
        model = TransactionHistory
        fields = ['id', 'owner', 'amount', 'created_time', 'kind']








