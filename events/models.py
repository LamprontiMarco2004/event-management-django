from django.conf import settings
from django.db import models
from django.urls import reverse


class Event(models.Model):
    """Un evento creato e gestito da un organizzatore.

    Relazione 1: ogni evento ha un organizer (ForeignKey verso l'utente).
    """

    title = models.CharField(max_length=200, verbose_name="Titolo")
    description = models.TextField(verbose_name="Descrizione")
    date = models.DateTimeField(verbose_name="Data e ora")
    location = models.CharField(max_length=200, verbose_name="Luogo")
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="events_organized",
        verbose_name="Organizzatore",
    )

    class Meta:
        # Eventi ordinati per data (i più imminenti in cima).
        ordering = ["date"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """URL del dettaglio evento: usato per i redirect DRY dopo create/update."""
        return reverse("events:event_detail", kwargs={"pk": self.pk})


class Registration(models.Model):
    """Iscrizione di un partecipante a un evento.

    Fa da tabella-ponte tra utente ed evento.
    Relazione 2: due ForeignKey (verso Event e verso l'utente partecipante).
    """

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="registrations",
        verbose_name="Evento",
    )
    attendee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="registrations",
        verbose_name="Partecipante",
    )
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name="Iscritto il")

    class Meta:
        ordering = ["-registered_at"]
        # Impedisce a uno stesso utente di iscriversi due volte allo stesso evento.
        unique_together = ("event", "attendee")

    def __str__(self):
        return f"{self.attendee} → {self.event}"
