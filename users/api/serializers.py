from rest_framework import serializers

from ..models import CustomeUserModel, MemberShip, Wallet


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = CustomeUserModel
        fields = ['username', 'email', 'year_of_birth',  'month_of_birth', 'day_of_birth', 'password', 'password2', 'country']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = CustomeUserModel(
                username = self.validated_data['username'],
                email=self.validated_data['email'],
                year_of_birth=self.validated_data['year_of_birth'],
                month_of_birth=self.validated_data['month_of_birth'],
                day_of_birth=self.validated_data['day_of_birth'],
                country=self.validated_data['country']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user


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

#     password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

#     class Meta:
#         model = CustomeUserModel
#         fields = ['email', 'username', 'password', 'password2', 'country']
#         extra_kwargs = {
#             'password': {'write_only': True},
#         }	


#     def validate(self, attrs):
#         if self.password == self.password2 and self.passsword != None and self.passowrd != '':
#             raise serializers.ValidationError(f"passwords are none or not equal to each other")
#         return super().validate(attrs)
    
#     def create(self, validated_data):
#         password2 = validated_data.pop('password2')
#         obj = super().create(validated_data)
#         print(password2, obj)
#         return obj