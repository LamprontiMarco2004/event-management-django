from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Utente personalizzato del progetto.

    Eredita da AbstractUser, quindi mantiene tutti i campi standard di Django
    (username, password, email, first_name, last_name, gruppi e permessi).
    Definirlo fin dall'inizio ci permette di estenderlo in futuro senza dover
    resettare le migrazioni. I ruoli Organizer/Attendee saranno gestiti tramite
    i Gruppi di Django (creati nella fase di autenticazione).
    """

    # Campo extra opzionale: una breve biografia mostrata nel profilo.
    bio = models.TextField(blank=True, verbose_name="Biografia")

    def __str__(self):
        return self.username
