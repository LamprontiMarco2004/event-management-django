from django.urls import path

from . import views

app_name = "events"

urlpatterns = [
    # CRUD eventi
    path("", views.EventListView.as_view(), name="event_list"),
    path("events/<int:pk>/", views.EventDetailView.as_view(), name="event_detail"),
    path("events/new/", views.EventCreateView.as_view(), name="event_create"),
    path("events/<int:pk>/edit/", views.EventUpdateView.as_view(), name="event_update"),
    path("events/<int:pk>/delete/", views.EventDeleteView.as_view(), name="event_delete"),
    # Pagine per ruolo
    path("my-events/", views.MyEventsView.as_view(), name="my_events"),
    path("my-registrations/", views.MyRegistrationsView.as_view(), name="my_registrations"),
    path("events/<int:pk>/participants/", views.EventParticipantsView.as_view(), name="participants"),
    # Iscrizione / annullamento
    path("events/<int:pk>/register/", views.register_to_event, name="register"),
    path("events/<int:pk>/unregister/", views.unregister_from_event, name="unregister"),
]
