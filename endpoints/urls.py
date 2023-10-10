from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CrosswalkModelViewSet, TrafficModelViewSet, CCTVModelViewSet


urlpatterns = []
# ./api/crosswalk/.
router = DefaultRouter()
router.register(r'crosswalk', CrosswalkModelViewSet)
urlpatterns.append(path('api/', include(router.urls)))

# ./api/traffic/.
router = DefaultRouter()
router.register(r'traffic', TrafficModelViewSet)
urlpatterns.append(path('api/', include(router.urls)))

# ./api/cctv/.
router = DefaultRouter()
router.register(r'cctv', CCTVModelViewSet)
urlpatterns.append(path('api/', include(router.urls)))