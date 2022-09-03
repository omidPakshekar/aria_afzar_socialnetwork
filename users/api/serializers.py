from urllib import request
from rest_framework import exceptions, serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

from ..models import CustomeUserModel, MemberShip, ProfileImage, UserBio, Wallet

from django.contrib.auth import authenticate, get_user_model
from dj_rest_auth.serializers import JWTSerializerWithExpiration
from django_countries.serializers import CountryFieldMixin
from django_countries.serializer_fields import CountryField


    
class CustomRegisterSerializer(RegisterSerializer):
    name            = serializers.CharField(max_length=30)
    gender          = serializers.CharField(max_length=1)
    year_of_birth   = serializers.CharField(max_length=20)
    month_of_birth  = serializers.CharField(max_length=20)
    day_of_birth    = serializers.CharField(max_length=20)
    country         = CountryField()
    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['name'] = self.validated_data.get('name')
        data_dict['country'] = self.validated_data.get('country')
        data_dict['gender'] = self.validated_data.get('gender')
        data_dict['year_of_birth'] = self.validated_data.get('year_of_birth')
        data_dict['month_of_birth'] = self.validated_data.get('month_of_birth')
        data_dict['day_of_birth'] = self.validated_data.get('day_of_birth')
        return data_dict


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_email(self, email, password):
        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = 'Must include "email" and "password".'
            raise exceptions.ValidationError(msg)
        return user
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        print('eamil', email, 'password', password)
        user = self.authenticate(username=email, password=password)
        print(user)
        if not user:
            msg = 'Unable to log in with provided credentials.'
            raise exceptions.ValidationError(msg)
        attrs['user'] = user
        return attrs


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"}, required=True)
    new_password = serializers.CharField(style={"input_type": "password"}, required=True)

"""
    wallet serializer
"""

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['amount', 'user']

""""
    membership serializer
"""
class MembershipCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberShip
        fields = ['month', ]

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberShip
        exclude = ['user', 'id']

"""
    CustomeUserModel serializer
"""
class BioInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBio
        fields = "__all__"

class ImageInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = "__all__"

class UserBioSerializer(serializers.ModelSerializer):
    user_bio = serializers.SerializerMethodField(source='user_bio', read_only=True)
    profile_pic = serializers.SerializerMethodField(source='profile_pic', read_only=True)
    class Meta:
        model = CustomeUserModel
        fields = ['name', 'username', 'email', 'profile_pic']
    def get_user_bio(self, obj):
        if not (obj.user_bio.admin_check or self.context['request'].user.is_admin):
            return ''
        return BioInlineSerializer(instance=obj.user_bio).data
    def get_profile_pic(self, obj):
        if not (obj.profile_pic.admin_check or self.context['request'].user.is_admin):
            return self.context['request'].build_absolute_uri('/media/default_image.jpg')
        return ImageInlineSerializer(instance=obj.profile_pic, context={'request' : self.context['request']}).data
        
class UserProfileSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField(source='profile_pic', read_only=True)
    country     = CountryField(name_only=True)
    flag        = serializers.SerializerMethodField(source='country')
    class Meta:
        model = CustomeUserModel
        fields = ['name', 'username', 'email', 'profile_pic', 'country', 'flag']
    
    def get_profile_pic(self, obj):
        request = self.context['request']
        if not (obj.profile_pic.admin_check or self.context['request'].user.is_admin):
            return request.build_absolute_uri('/media/default_image.jpg')
        return ImageInlineSerializer(instance=obj.profile_pic, context={'request' : request}).data
    def get_flag(self, obj):
        return self.context['request'].build_absolute_uri(obj.country.flag)        


class UserAllInfoSerializer( serializers.ModelSerializer):
    user_bio    = serializers.SerializerMethodField(source='user_bio', read_only=True)
    profile_pic = serializers.SerializerMethodField(source='profile_pic', read_only=True)
    country     = CountryField(name_only=True)
    flag        = serializers.SerializerMethodField(source='country')
    class Meta:
        model = CustomeUserModel
        fields = ['name', 'username', 'email', 'profile_pic', 'date_joined', 'last_login',
                    'gender', 'country', 'flag', 'have_membership', 'user_bio', 'profile_pic',
                    'year_of_birth', 'month_of_birth', 'day_of_birth']
    def get_user_bio(self, obj):
        request =  self.context['request']
        if not (obj == request.user or obj.user_bio.admin_check or request.user.is_admin):
            return ''
        return BioInlineSerializer(instance=obj.user_bio).data
    def get_profile_pic(self, obj):
        request =  self.context['request']
        if not (obj == request.user or obj.profile_pic.admin_check or request.user.is_admin):
            return request.build_absolute_uri('/media/default_image.jpg')
        return ImageInlineSerializer(instance=obj.profile_pic, context={'request' : self.context['request']}).data
    
    def get_flag(self, obj):
        return self.context['request'].build_absolute_uri(obj.country.flag)

class UserSeenInfoSerializer(serializers.ModelSerializer):
    user_bio    = serializers.SerializerMethodField(source='user_bio', read_only=True)
    profile_pic = serializers.SerializerMethodField(source='profile_pic', read_only=True)
    country     = CountryField(name_only=True)
    flag        = serializers.SerializerMethodField(source='country')

    class Meta:
        model = CustomeUserModel
        fields = ['name', 'username', 'profile_pic', 'user_bio', 'gender', 'country', 'flag']
    def get_user_bio(self, obj):
        if not (obj.user_bio.admin_check or self.context['request'].user.is_admin):
            return ''
        return BioInlineSerializer(instance=obj.user_bio).data
    def get_profile_pic(self, obj):
        if not (obj.profile_pic.admin_check or self.context['request'].user.is_admin):
            return self.context['request'].build_absolute_uri('/media/default_image.jpg')
        return ImageInlineSerializer(instance=obj.profile_pic, context={'request' : self.context['request']}).data
    def get_flag(self, obj):
        return self.context['request'].build_absolute_uri(obj.country.flag)
class UserUpdateSerializer(serializers.ModelSerializer):
    country     = CountryField(name_only=True)
    class Meta:
        model = CustomeUserModel
        fields = ['name', 'gender', 'country', 'year_of_birth',
                 'month_of_birth', 'day_of_birth']


# for UserCustomLogin
class CustomJWTSerializer(JWTSerializerWithExpiration):
    user = serializers.SerializerMethodField()
    def get_user(self, obj):
        return UserAllInfoSerializer(instance=obj['user'], context={'request' : self.context['request']}).data

class UpdateBioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBio
        fields = ['bio']


class UpdateProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = ['image']
        

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






