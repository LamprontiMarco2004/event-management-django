from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    """Registrazione di un nuovo utente (generic class-based view).

    Dopo la creazione, l'utente viene assegnato al gruppo 'Attendee' e
    reindirizzato alla pagina di login."""

    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        # Salva l'utente e lo aggiunge al gruppo Attendee (ruolo di default).
        response = super().form_valid(form)
        attendee_group = Group.objects.get(name="Attendee")
        self.object.groups.add(attendee_group)
        return response
