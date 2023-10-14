from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import CrosswalkModel, TrafficModel, CCTVModel
from .serializers import CrosswalkModelSerializer, TrafficModelSerializer, CCTVModelSerializer


def find_crosswalk_by_distance(point : Point, cnt : int, traffic : bool):
    '''
    거리순으로 횡단보도를 찾는 알고리즘(postgis 내부 알고리즘 이용)
    '''
    
    # 신호등 유무 확인
    if traffic:
        crosswalk = CrosswalkModel.objects.all()
    else:
        crosswalk = CrosswalkModel.objects.filter(traffic=False)
    
    # 거리에 따라 재배열
    crosswalk = (
            crosswalk.annotate(distance=Distance("geom", point))
            .order_by("distance")
        )
    crosswalk_with_distance = crosswalk.values('id', 'geom', 'traffic', 'cctv', 'distance_to_cctv', 'distance')[:cnt]
    return crosswalk_with_distance


def find_crosswalk_by_radius(point : Point, radius : float, traffic : bool):
    '''
    일정 거리 안 모든 횡단보도를 찾는 알고리즘(postgis 내부 알고리즘 이용)
    '''
    
    # 신호등 유무 확인
    if traffic:
        crosswalk = CrosswalkModel.objects.all()
    else:
        crosswalk = CrosswalkModel.objects.filter(traffic=False)
    
    # 거리 내에 있는지 확인
    crosswalk = crosswalk.filter(geom__distance_lte=(point, D(m=radius)))
    
    # 거리 계산
    crosswalk = (
        crosswalk.annotate(distance=Distance("geom", point))
        .order_by("distance")
    )
    crosswalk_with_distance = crosswalk.values('id', 'geom', 'traffic', 'cctv', 'distance_to_cctv', 'distance')
    return crosswalk_with_distance
    
    

class CrosswalkModelViewSet(viewsets.ModelViewSet):
    queryset = CrosswalkModel.objects.all()
    serializer_class = CrosswalkModelSerializer

    # post요청 무시
    def create(self, request, *args, **kwargs):
        return Response({'detail': 'Method \"POST\" not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @action(detail=False, methods=['post'], url_path='find/distance')
    def find_by_distance(self, request):
        '''
        body로 받은 좌표값에 대해 거리순으로 횡단보도를 반환한다.
        latitude: 위도(float)
        longitude: 경도(float)
        cnt: 반환할 개수(int)
        traffic: false - 신호등 없는 횡단보도만 조회 true - 신호등 있는 횡단보도도 조회(bool)
        '''
        
        # body가 올바른지 확인
        json_data = request.data
        try:
            latitude, longitude, cnt, traffic = (
                float(json_data['latitude']),
                float(json_data['longitude']),
                int(json_data['count']),
                bool(json_data['traffic']),
            )
        except Exception as e:
            return Response(
                {'detail': f'{str(e)}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        # body 받은 좌푯값을 Point객체로 변경
        point = Point(longitude, latitude, srid=4326)
        
        # 거리순으로 횡단보도 찾기
        crosswalk = find_crosswalk_by_distance(point, cnt, traffic)
        # 수행에 성공했으면 반환, 못했으면 404오류
        if crosswalk:
            response = {'count': len(crosswalk), 'crosswalk': {}}
            for idx, data in enumerate(crosswalk):
                response['crosswalk'][idx] = {
                    'id': data['id'],
                    'geom': str(data['geom']),
                    'traffic': bool(data['traffic']),
                    'cctv': data['cctv'],
                    'distance_to_cctv': data['distance_to_cctv'],
                    'distance': data['distance'].m
                }
            return Response(response)
        else:
            return Response(
                {'detail': 'No matching crosswalk found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
    
    @action(detail=False, methods=['post'], url_path='find/radius')
    def find_within_radius(self, request):
        '''
        body로 받은 좌표값에 대해 거리내 횡단보도를 반환한다.
        latitude: 위도(float)
        longitude: 경도(float)
        radius: 탐색 범위(float)
        traffic: 신호등 있는 횡단보도도 조회(bool)
        '''
        # body가 올바른지 확인
        json_data = request.data
        try:
            latitude, longitude, radius, traffic = (
                float(json_data['latitude']),
                float(json_data['longitude']),
                float(json_data['radius']),
                bool(json_data['traffic']),
            )
        except Exception as e:
            return Response(
                {'detail': f'{str(e)}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # body 받은 좌푯값을 Point객체로 변경
        point = Point(longitude, latitude, srid=4326)
        
        # 거리내 횡단보도 찾기
        crosswalk = find_crosswalk_by_radius(point, radius, traffic)
        # 수행에 성공했으면 반환, 못했으면 404오류
        if crosswalk:
            response = {'count': len(crosswalk), 'crosswalk': {}}
            for idx, data in enumerate(crosswalk):
                response['crosswalk'][idx] = {
                    'id': data['id'],
                    'geom': str(data['geom']),
                    'traffic': bool(data['traffic']),
                    'cctv': data['cctv'],
                    'distance_to_cctv': data['distance_to_cctv'],
                    'distance': data['distance'].m
                }
            return Response(response)
        else:
            return Response(
                {'detail': 'No matching crosswalk found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        
    

class TrafficModelViewSet(viewsets.ModelViewSet):
    queryset = TrafficModel.objects.all()
    serializer_class = TrafficModelSerializer
    
    # post요청 무시
    def create(self, request, *args, **kwargs):
        return Response({'detail': 'Method \"POST\" not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CCTVModelViewSet(viewsets.ModelViewSet):
    queryset = CCTVModel.objects.all()
    serializer_class = CCTVModelSerializer

    # post요청 무시
    def create(self, request, *args, **kwargs):
        return Response({'detail': 'Method \"POST\" not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    