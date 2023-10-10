from rest_framework import serializers
from .models import CrosswalkModel, TrafficModel, CCTVModel

class CrosswalkModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrosswalkModel
        fields = '__all__'


class TrafficModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficModel
        fields = '__all__'


class CCTVModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CCTVModel
        fields = '__all__'