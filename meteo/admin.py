from django.contrib import admin
from .models import ReleveMeteo

@admin.register(ReleveMeteo)
class ReleveMeteoAdmin(admin.ModelAdmin):
    list_display = ('ville', 'date', 'temperature_2m_mean', 'precipitation_sum', 'wind_speed_10m_max')
    list_filter = ('date', 'ville__region') 
    search_fields = ('ville__nom',)
    date_hierarchy = 'date' 