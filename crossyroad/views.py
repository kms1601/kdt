from rest_framework import viewsets
from .models import Crosswalk
from .serializers import CrosswalkSerializer

class CrosswalkViewSet(viewsets.ModelViewSet):
    queryset = Crosswalk.objects.all()[:200]
    serializer_class = CrosswalkSerializer
    