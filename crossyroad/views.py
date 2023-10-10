from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import CrosswalkModel, TrafficModel, CCTVModel
from .serializers import CrosswalkModelSerializer, TrafficModelSerializer, CCTVModelSerializer


class CrosswalkModelViewSet(viewsets.ModelViewSet):
    queryset = CrosswalkModel.objects.all()
    serializer_class = CrosswalkModelSerializer
    
    @action(detail=False, methods=['post'], url_path='find')
    def find_closest_crosswalk(self, request):
        try:
            latitude = float(request.GET['latitude'])
            longitude = float(request.GET['longitude'])
        except:
            return Response({'message': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        
        point = Point(longitude, latitude, srid=4326)
        
        closest_crosswalk = CrosswalkModel.objects.annotate(
            distance=Distance('geom', point)
        ).order_by('distance').first()
        
        if closest_crosswalk:
            serializer = CrosswalkModelSerializer(closest_crosswalk)
            distance = closest_crosswalk.distance.m
            return Response({'crosswalk': serializer.data, 'distance': distance})
        else:
            return Response({'message': 'No matching crosswalk found.'}, status=status.HTTP_404_NOT_FOUND)


class TrafficModelViewSet(viewsets.ModelViewSet):
    queryset = TrafficModel.objects.all()
    serializer_class = TrafficModelSerializer


class CCTVModelViewSet(viewsets.ModelViewSet):
    queryset = CCTVModel.objects.all()
    serializer_class = CCTVModelSerializer
