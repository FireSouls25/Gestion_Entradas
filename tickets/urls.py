from django.urls import path
from .views import generate_qr_code, validate_ticket

urlpatterns = [
    path('<int:ticket_id>/qr/', generate_qr_code, name='generate-qr-code'),
    path('<int:ticket_id>/validate/', validate_ticket, name='validate-ticket'),
]
