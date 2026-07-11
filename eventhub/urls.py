"""URL configuration for eventhub project."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Autenticazione: signup, login, logout (app accounts).
    path("accounts/", include("accounts.urls")),
    # Eventi: la lista è la home page del sito.
    path("", include("events.urls")),
]
