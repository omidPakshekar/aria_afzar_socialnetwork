from rest_framework import serializers

from ..models import SuccessfullExperience
from payment.api.serializers import UserInlineSerializer

class ExprienceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessfullExperience
        fields = ['title', 'description']



class ExprienceAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessfullExperience
        fields = ['title', 'description', 'admin_check']



class ExprienceSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    save_number = serializers.SerializerMethodField(read_only=True)
    owner = UserInlineSerializer(read_only=True)
    class Meta:
        model = SuccessfullExperience
        fields = ['owner', 'title', 'description', 'likes', 'save_number']

    def get_likes(self, obj):
        return obj.user_liked.count()

    def get_save_number(self, obj):
        return obj.user_saved.count()

# class ExprienceChangeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SuccessfullExperience
#         fields = 







