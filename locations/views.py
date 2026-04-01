from rest_framework import viewsets, permissions
from .models import Region, Ville
from .serializers import RegionSerializer, VilleSerializer

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class VilleViewSet(viewsets.ModelViewSet):
    queryset = Ville.objects.select_related('region').all()
    serializer_class = VilleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]