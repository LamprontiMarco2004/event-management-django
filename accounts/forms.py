from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Form di registrazione basato sul nostro CustomUser.

    Estende UserCreationForm di Django (che gestisce già le due password e la
    loro validazione) e lo aggancia al modello utente personalizzato, aggiungendo
    il campo email tra quelli richiesti."""

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Campi espliciti (mai '__all__'): username + email, più le password
        # gestite automaticamente da UserCreationForm.
        fields = ("username", "email")
