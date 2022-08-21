from rest_framework import serializers

from ..models import CustomeUserModel, MemberShip, Wallet

from dj_rest_auth.registration.serializers import RegisterSerializer


class CustomRegisterSerializer(RegisterSerializer):
    country         = serializers.CharField(max_length=20)
    gender          = serializers.CharField(max_length=4)
    year_of_birth   = serializers.CharField(max_length=20)
    month_of_birth  = serializers.CharField(max_length=20)
    day_of_birth    = serializers.CharField(max_length=20)


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"}, required=True)
    new_password = serializers.CharField(style={"input_type": "password"}, required=True)

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['amount', 'user']


class MembershipCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberShip
        fields = ['month', ]

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberShip
        exclude = ['user', 'id']




# class RegistrationSerializer(serializers.ModelSerializer):
#     password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

#     class Meta:
#         model = CustomeUserModel
#         fields = ['username', 'email', 'year_of_birth',  'month_of_birth', 'day_of_birth', 'password', 'password2', 'country']
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }

#     def save(self):
#         user = CustomeUserModel(
#                 username = self.validated_data['username'],
#                 email=self.validated_data['email'],
#                 year_of_birth=self.validated_data['year_of_birth'],
#                 month_of_birth=self.validated_data['month_of_birth'],
#                 day_of_birth=self.validated_data['day_of_birth'],
#                 country=self.validated_data['country']
#         )
#         password = self.validated_data['password']
#         password2 = self.validated_data['password2']
#         if password != password2:
#             raise serializers.ValidationError({'password': 'Passwords must match.'})
#         user.set_password(password)
#         user.save()
#         return user






