from django.urls import path
from .views import generate_qr_code, validate_ticket, purchase_ticket_view, my_tickets_view

app_name = 'tickets'

urlpatterns = [
    path('<int:ticket_id>/qr/', generate_qr_code, name='generate-qr-code'),
    path('<int:ticket_id>/validate/', validate_ticket, name='validate-ticket'),
    path('event/<int:event_id>/purchase/', purchase_ticket_view, name='purchase-ticket'),
    path('my-tickets/', my_tickets_view, name='my-tickets'),
    path('my-tickets/event/<int:event_id>/', my_tickets_view, name='my-tickets-event'),
]
