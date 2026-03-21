from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur

@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'langue_preferee', 'is_staff')
    list_filter = ('role', 'langue_preferee', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    filter_horizontal = ('villes_favorites',)

    fieldsets = UserAdmin.fieldsets + (
        ('Informations AirGuard', {
            'fields': ('role', 'fcm_token', 'langue_preferee', 'villes_favorites')
        }),
    )