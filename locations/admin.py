from django.contrib import admin
from .models import Region, Ville

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom')
    search_fields = ('nom',)

@admin.register(Ville)
class VilleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'region', 'latitude', 'longitude')
    list_filter = ('region',) 
    search_fields = ('nom',)