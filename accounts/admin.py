from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Riusa l'admin standard di Django (gestione corretta di password e gruppi),
    aggiungendo il campo extra 'bio' nella sezione del profilo."""

    fieldsets = UserAdmin.fieldsets + (
        ("Profilo", {"fields": ("bio",)}),
    )
