from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import EventForm
from .models import Event, Registration


# ---------------------------------------------------------------------------
# CRUD eventi (generic class-based view)
# ---------------------------------------------------------------------------

class EventListView(ListView):
    """Lista di tutti gli eventi: è la home page, visibile anche senza login."""

    model = Event
    template_name = "events/event_list.html"
    context_object_name = "events"


class EventDetailView(DetailView):
    """Dettaglio di un singolo evento."""

    model = Event
    template_name = "events/event_detail.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        # Dice al template se l'utente loggato è già iscritto a questo evento,
        # per mostrare il pulsante "Iscriviti" oppure "Annulla iscrizione".
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["is_registered"] = (
            user.is_authenticated
            and self.object.registrations.filter(attendee=user).exists()
        )
        return context


class EventCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Creazione evento: riservata agli utenti del gruppo Organizer.

    LoginRequiredMixin va per primo nell'ereditarietà: prima si verifica che
    l'utente sia loggato, poi (UserPassesTestMixin) che abbia il ruolo giusto."""

    model = Event
    form_class = EventForm
    template_name = "events/event_form.html"

    def test_func(self):
        return self.request.user.is_organizer

    def form_valid(self, form):
        # L'organizzatore è sempre l'utente loggato (non arriva dal form).
        form.instance.organizer = self.request.user
        messages.success(self.request, "Evento creato con successo.")
        return super().form_valid(form)
        # Il redirect usa get_absolute_url() del modello (dettaglio evento).


class OrganizerOwnsEventMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Permesso condiviso da modifica ed eliminazione: solo il proprietario.

    test_func confronta l'organizer dell'evento con l'utente loggato; se il
    test fallisce Django solleva PermissionDenied -> pagina 403."""

    def test_func(self):
        return self.get_object().organizer == self.request.user


class EventUpdateView(OrganizerOwnsEventMixin, UpdateView):
    """Modifica evento: solo l'organizzatore che lo ha creato."""

    model = Event
    form_class = EventForm
    template_name = "events/event_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Evento aggiornato con successo.")
        return super().form_valid(form)


class EventDeleteView(OrganizerOwnsEventMixin, DeleteView):
    """Eliminazione evento (con pagina di conferma): solo il proprietario."""

    model = Event
    template_name = "events/event_confirm_delete.html"
    success_url = reverse_lazy("events:event_list")

    def form_valid(self, form):
        messages.success(self.request, "Evento eliminato.")
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# Pagine per ruolo
# ---------------------------------------------------------------------------

class MyEventsView(LoginRequiredMixin, ListView):
    """'I miei eventi': gli eventi creati dall'organizzatore loggato."""

    template_name = "events/my_events.html"
    context_object_name = "events"

    def get_queryset(self):
        return self.request.user.events_organized.all()


class MyRegistrationsView(LoginRequiredMixin, ListView):
    """'Le mie iscrizioni': gli eventi a cui il partecipante si è iscritto."""

    template_name = "events/my_registrations.html"
    context_object_name = "registrations"

    def get_queryset(self):
        return self.request.user.registrations.select_related("event")


class EventParticipantsView(OrganizerOwnsEventMixin, DetailView):
    """Lista dei partecipanti a un evento: solo per il suo organizzatore."""

    model = Event
    template_name = "events/participants.html"
    context_object_name = "event"


# ---------------------------------------------------------------------------
# Iscrizione / annullamento (function view: azioni semplici, solo POST)
# ---------------------------------------------------------------------------

@login_required
def register_to_event(request, pk):
    """Iscrive l'utente loggato all'evento (se non è il suo organizzatore)."""
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        if event.organizer == request.user:
            messages.error(request, "Non puoi iscriverti a un tuo evento.")
        else:
            # get_or_create evita doppie iscrizioni (insieme a unique_together).
            _, created = Registration.objects.get_or_create(
                event=event, attendee=request.user
            )
            if created:
                messages.success(request, f"Iscrizione a «{event.title}» confermata.")
            else:
                messages.info(request, "Sei già iscritto a questo evento.")
    return redirect(event.get_absolute_url())


@login_required
def unregister_from_event(request, pk):
    """Annulla l'iscrizione dell'utente loggato all'evento."""
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        deleted, _ = Registration.objects.filter(
            event=event, attendee=request.user
        ).delete()
        if deleted:
            messages.success(request, f"Iscrizione a «{event.title}» annullata.")
    return redirect(event.get_absolute_url())
