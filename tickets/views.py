import qrcode
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Ticket

def generate_qr_code(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"Ticket ID: {ticket.id}\nAttendee: {ticket.attendee.username}\nEvent: {ticket.ticket_type.event.title}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages

def is_organizer(user):
    return user.is_authenticated and user.userprofile.role == 'organizer'

@user_passes_test(is_organizer)
def validate_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        if not ticket.is_validated:
            ticket.is_validated = True
            ticket.save()
            messages.success(request, 'Entrada validada exitosamente.')
        else:
            messages.warning(request, 'Esta entrada ya ha sido validada.')
        return redirect('events:event-detail', pk=ticket.ticket_type.event.pk)
    
    return render(request, 'tickets/validate_ticket.html', {'ticket': ticket})