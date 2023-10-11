from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CrosswalkModelViewSet, TrafficModelViewSet, CCTVModelViewSet


router = DefaultRouter()
router.register(r'crosswalk', CrosswalkModelViewSet)
router.register(r'traffic', TrafficModelViewSet)
router.register(r'cctv', CCTVModelViewSet)
urlpatterns = [
    path('api/', include(router.urls))
]
