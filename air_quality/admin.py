from django.contrib import admin
from .models import QualiteAir

@admin.register(QualiteAir)
class QualiteAirAdmin(admin.ModelAdmin):
    list_display = ('ville', 'date_cible', 'indice_aqi', 'categorie', 'est_prediction')
    list_filter = ('categorie', 'est_prediction', 'ville__region')
    search_fields = ('ville__nom',)
    date_hierarchy = 'date_cible'