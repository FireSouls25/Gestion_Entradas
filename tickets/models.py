from django.db import models
from django.contrib.auth.models import User
from events.models import TicketType

class Ticket(models.Model):
    attendee = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    purchase_time = models.DateTimeField(auto_now_add=True)
    qr_code = models.CharField(max_length=255, blank=True, null=True) # Store path to QR code or the code itself
    is_validated = models.BooleanField(default=False)

    def __str__(self):
        return f'Ticket for {self.attendee.username} - {self.ticket_type.name}'
