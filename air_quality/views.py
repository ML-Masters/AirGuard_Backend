from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg 
from django.utils import timezone
from .models import QualiteAir
from .serializers import QualiteAirSerializer

class QualiteAirViewSet(viewsets.ModelViewSet):
    queryset = QualiteAir.objects.all().order_by('-date_cible')
    serializer_class = QualiteAirSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ['ville__nom', 'date_cible', 'est_prediction', 'categorie']

    @action(detail=False, methods=['get'], url_path='national_kpis')
    def get_national_kpis(self, request):
        aujourd_hui = timezone.now().date()
        
        donnees_jour = QualiteAir.objects.filter(
            date_cible=aujourd_hui, 
            est_prediction=False
        )

        if not donnees_jour.exists():
            return Response({"message": "Aucune donnée disponible pour aujourd'hui."}, status=200)

        aqi_moyen = donnees_jour.aggregate(Avg('indice_aqi'))['indice_aqi__avg']

        villes_en_danger = donnees_jour.filter(
            categorie__in=['Malsain', 'Tres_malsain', 'Dangereux']
        ).count()

        return Response({
            "date": aujourd_hui,
            "aqi_moyen_national": round(aqi_moyen, 2) if aqi_moyen else 0,
            "nombre_villes_critiques": villes_en_danger,
            "total_villes_scannees": donnees_jour.count()
        })