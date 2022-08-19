from rest_framework import serializers

from ..models import SuccessfullExperience

class ExprienceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessfullExperience
        fields = ['title', 'description']















