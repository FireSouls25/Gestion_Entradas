import qrcode
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Ticket
from events.models import TicketType, Event
from events.forms import TicketPurchaseForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
import random

def my_tickets_view(request):
    tickets = Ticket.objects.filter(attendee=request.user)
    return render(request, 'tickets/my_tickets.html', {'tickets': tickets})

def simulate_payment_api(amount):
    # Simulate a payment API call
    # In a real application, this would interact with a payment gateway
    if random.choice([True, False]):  # 50% chance of success
        return {'status': 'success', 'transaction_id': 'txn_' + str(random.randint(10000, 99999))}
    else:
        return {'status': 'failed', 'error': 'Payment failed due to an unknown error.'}

@login_required
def purchase_ticket_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    ticket_types = TicketType.objects.filter(event=event)

    if request.method == 'POST':
        form = TicketPurchaseForm(request.POST)
        form.fields['ticket_type'].queryset = ticket_types
        if form.is_valid():
            ticket_type = form.cleaned_data['ticket_type']
            quantity = form.cleaned_data['quantity']

            if ticket_type.quantity < quantity:
                messages.error(request, 'No hay suficientes entradas disponibles de este tipo.')
                return redirect('events:event-detail', pk=event_id)
            
            total_amount = ticket_type.price * quantity
            payment_result = simulate_payment_api(total_amount)

            if payment_result['status'] == 'success':
                for _ in range(quantity):
                    Ticket.objects.create(
                        attendee=request.user,
                        ticket_type=ticket_type,
                    )
                ticket_type.quantity -= quantity
                ticket_type.save()
                messages.success(request, 'Compra de entradas exitosa!')
                return redirect('tickets:my-tickets') # Redirect to my tickets page
            else:
                messages.error(request, f'Error en el pago: {payment_result['error']}')
        else:
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else:
        form = TicketPurchaseForm()
        form.fields['ticket_type'].queryset = ticket_types

    return render(request, 'tickets/purchase_ticket.html', {'form': form, 'event': event, 'ticket_types': ticket_types})

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
    return response

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