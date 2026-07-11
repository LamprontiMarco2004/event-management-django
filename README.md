# EventHub — Event Management System

**Studente:** Marco Lampronti
**Esame:** Produzione e Progettazione Multimediale — secondo parziale (Backend con Django)

- **Tipo di progetto:** Full-Stack Web Application
- **Framework:** Django (Django Template Language + Bootstrap 5)
- **Track:** Event Management System

## Descrizione e scopo

EventHub è una piattaforma per la gestione di eventi: gli **organizzatori** creano e gestiscono eventi, i **partecipanti** li sfogliano e si iscrivono. Il progetto dimostra un back-end Django completo: modello dati relazionale, custom user model, ruoli con permessi enforced nel codice, CRUD con class-based view, form validati e interfaccia che cambia in base al ruolo.

## Funzionalità per ruolo

**Visitatore (non autenticato)**
- Sfoglia la lista eventi e il dettaglio di ogni evento
- Si registra al sito (diventa automaticamente Attendee) e fa login

**Attendee (partecipante)**
- Si iscrive a un evento e annulla l'iscrizione
- Consulta "Le mie iscrizioni"
- Non può creare, modificare o eliminare eventi (403 se ci prova)

**Organizer (organizzatore)**
- Crea nuovi eventi
- Modifica ed elimina **solo i propri** eventi (403 sugli eventi altrui)
- Consulta "I miei eventi" e la lista dei partecipanti ai propri eventi

**Amministratore**
- Accesso completo alla dashboard `/admin/` (gestione utenti, gruppi, eventi)

## Architettura (mappa sui requisiti)

- **2 app Django:** `accounts` (custom user + autenticazione) ed `events` (eventi e iscrizioni)
- **2 relazioni:** `Event.organizer` → utente (FK); `Registration` → tabella ponte con FK verso `Event` e verso l'utente, con `unique_together` anti doppia iscrizione
- **Custom user model:** `CustomUser(AbstractUser)` con `AUTH_USER_MODEL`
- **Ruoli:** Gruppi Django `Organizer` e `Attendee`, creati da una data migration; permessi enforced con `LoginRequiredMixin` + `UserPassesTestMixin`
- **Class-based view:** CRUD eventi con generic view (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`)
- **Validazione:** `ModelForm` con campi espliciti e messaggi d'errore nel template

## Installazione locale

```bash
git clone https://github.com/LamprontiMarco2004/event-management-django.git
cd event-management-django
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Apri poi <http://127.0.0.1:8000>.

**Database:** la repo include `db.sqlite3` già popolato con i dati e gli account demo, quindi il sito è utilizzabile subito. In alternativa i dati si possono ricaricare da zero con:

```bash
python manage.py loaddata demo_data
```

## Account demo

| Username | Password | Ruolo |
|---|---|---|
| `admin_demo` | `admin12345` | Superuser (accesso `/admin/`) |
| `organizer_demo` | `organizer12345` | Organizer |
| `attendee_demo` | `attendee12345` | Attendee |
| `marta_demo` | `marta12345` | Attendee |
| `luca_demo` | `luca12345` | Attendee |

*(Credenziali fittizie, create esclusivamente per la valutazione.)*

## Deploy

Applicazione online su Railway (PostgreSQL in produzione):

**🔗 <INSERIRE-LINK-RAILWAY>**

## Scenario di test dal browser

1. **Login come `organizer_demo`** → nella navbar compaiono "Crea evento" e "I miei eventi".
2. **Crea un evento** ("Crea evento", compila il form, salva) → redirect al dettaglio con messaggio di conferma. Prova anche a inviare il form con un campo vuoto: resta sul form con l'errore evidenziato.
3. **Modifica l'evento** dal pulsante "Modifica" nel dettaglio → il titolo aggiornato appare in lista.
4. **Logout e login come `attendee_demo`** → la navbar cambia ("Le mie iscrizioni", niente "Crea evento").
5. **Iscriviti a un evento** dal dettaglio → messaggio di conferma; l'evento appare in "Le mie iscrizioni".
6. **Azione vietata:** da `attendee_demo` visita l'URL di modifica di un evento, es. `/events/1/edit/` → **pagina 403 "Accesso negato"**: i permessi sono enforced nel codice, non solo nascosti dall'interfaccia.
7. **Rientra come `organizer_demo`** → dal dettaglio di un suo evento apri "Partecipanti" e verifica la lista degli iscritti.
