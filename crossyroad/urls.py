from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CrosswalkViewSet

router = DefaultRouter()
router.register(r'crosswalk-list', CrosswalkViewSet)

urlpatterns = [
    # 다른 URL 패턴들
    path('api/', include(router.urls)),
]
