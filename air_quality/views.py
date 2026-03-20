from rest_framework import viewsets, permissions
from .models import QualiteAir
from .serializers import QualiteAirSerializer

class QualiteAirViewSet(viewsets.ModelViewSet):
    queryset = QualiteAir.objects.all().order_by('-date_cible')
    serializer_class = QualiteAirSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ['ville__nom', 'date_cible', 'est_prediction', 'categorie']