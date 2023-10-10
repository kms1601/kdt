from rest_framework import serializers
from .models import Crosswalk

class CrosswalkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crosswalk
        fields = '__all__'
