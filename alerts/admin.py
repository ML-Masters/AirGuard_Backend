from django.contrib import admin
from .models import Alerte

@admin.register(Alerte)
class AlerteAdmin(admin.ModelAdmin):
    list_display = ('ville', 'niveau_severite', 'date_creation', 'est_active')
    list_filter = ('niveau_severite', 'est_active')
    search_fields = ('ville__nom', 'message_fr')
    list_editable = ('est_active',) 