from rest_framework import viewsets, permissions
from rest_framework.decorators import action 
from rest_framework.response import Response
from .models import Alerte
from .serializers import AlerteSerializer

class AlerteViewSet(viewsets.ModelViewSet):
    queryset = Alerte.objects.all().order_by('-date_creation')
    serializer_class = AlerteSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @action(detail=False, methods=['get'], url_path='active')
    def get_active_alerts(self, request):
        alertes_actives = self.queryset.filter(est_active=True)
        serializer = self.get_serializer(alertes_actives, many=True)
        return Response(serializer.data)