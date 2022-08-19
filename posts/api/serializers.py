from rest_framework import serializers

from ..models import SuccessfullExperience

class ExprienceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessfullExperience
        fields = ['title', 'description']


class ExprienceSerializer(serializers.ModelSerializer):
    # likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = SuccessfullExperience
        fields = ['title', 'description']

    # def get_likes(self, obj):
    #     return obj.user_liked.all().count()










