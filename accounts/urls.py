from django.contrib.auth import views as auth_views
from django.urls import path

from .views import SignUpView

urlpatterns = [
    # Registrazione (view personalizzata).
    path("signup/", SignUpView.as_view(), name="signup"),
    # Login e logout: view native di Django (nessun codice da riscrivere).
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
