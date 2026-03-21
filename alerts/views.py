from rest_framework import viewsets, permissions
from rest_framework.decorators import action 
from rest_framework.response import Response
from .models import Alerte
from .serializers import AlerteSerializer

from .services import envoyer_notification_push 
from users.models import Utilisateur 

class AlerteViewSet(viewsets.ModelViewSet):
    queryset = Alerte.objects.all().order_by('-date_creation')
    serializer_class = AlerteSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @action(detail=False, methods=['get'], url_path='active')
    def get_active_alerts(self, request):
        alertes_actives = self.queryset.filter(est_active=True)
        serializer = self.get_serializer(alertes_actives, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        alerte = serializer.save()

        if alerte.est_active:
            ville_concernee = alerte.ville
            
            utilisateurs = Utilisateur.objects.filter(
                villes_favorites=ville_concernee
            ).exclude(fcm_token__isnull=True).exclude(fcm_token__exact='')

            titre = f"Alerte AirGuard : {ville_concernee.nom}"
            message = alerte.message_fr

            for user in utilisateurs:
                envoyer_notification_push(
                    fcm_token=user.fcm_token,
                    titre=titre,
                    message=message,
                    data_supplementaire={
                        "ville_id": str(ville_concernee.id),
                        "severite": alerte.niveau_severite
                    }
                )