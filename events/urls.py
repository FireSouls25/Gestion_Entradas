from django.urls import path
from .views import (
    EventListView,
    EventDetailView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
    LocationListView,
    LocationCreateView,
    LocationUpdateView,
    LocationDeleteView,
    TicketTypeCreateView,
    TicketTypeUpdateView,
    TicketTypeDeleteView,
)

app_name = 'events'

urlpatterns = [
    path('', EventListView.as_view(), name='event-list'),
    path('<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('create/', EventCreateView.as_view(), name='event-create'),
    path('<int:pk>/update/', EventUpdateView.as_view(), name='event-update'),
    path('<int:pk>/delete/', EventDeleteView.as_view(), name='event-delete'),

    path('locations/', LocationListView.as_view(), name='location-list'),
    path('locations/create/', LocationCreateView.as_view(), name='location-create'),
    path('locations/<int:pk>/update/', LocationUpdateView.as_view(), name='location-update'),
    path('locations/<int:pk>/delete/', LocationDeleteView.as_view(), name='location-delete'),

    path('event/<int:event_pk>/ticket-types/create/', TicketTypeCreateView.as_view(), name='ticket-type-create'),
    path('ticket-types/<int:pk>/update/', TicketTypeUpdateView.as_view(), name='ticket-type-update'),
    path('ticket-types/<int:pk>/delete/', TicketTypeDeleteView.as_view(), name='ticket-type-delete'),
]
