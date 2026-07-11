from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    """ModelForm per creare/modificare un evento.

    Campi espliciti (mai '__all__'): l'organizer NON è nel form perché viene
    impostato automaticamente nella view dall'utente loggato — così nessuno
    può creare eventi a nome di altri."""

    class Meta:
        model = Event
        fields = ("title", "description", "date", "location")
        widgets = {
            # Input nativo del browser con selettore data+ora.
            "date": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_title(self):
        """Validazione custom: il titolo non può essere vuoto o di soli spazi."""
        title = self.cleaned_data["title"].strip()
        if not title:
            raise forms.ValidationError("Il titolo non può essere vuoto.")
        return title
