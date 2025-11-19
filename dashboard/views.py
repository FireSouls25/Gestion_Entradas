from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from events.models import Event, TicketType
from tickets.models import Ticket
from django.db.models import Count, Sum, F
from django.contrib import messages

@login_required
def dashboard_view(request):
    try:
        role = request.user.userprofile.role
        if role == 'organizer':
            events = Event.objects.filter(organizer=request.user)
            return render(request, 'dashboard/dashboard_organizer.html', {'events': events})
        elif role == 'attendee':
            assisted_events = Event.objects.filter(assistants=request.user)
            return render(request, 'dashboard/dashboard_attendee.html', {'assisted_events': assisted_events})
        elif role == 'client':
            return render(request, 'dashboard/dashboard_client.html')
    except AttributeError:
        # Handle cases where userprofile might not exist
        return render(request, 'dashboard.html')
    return render(request, 'dashboard.html')

@login_required
def event_statistics_view(request, event_id):
    event = Event.objects.get(id=event_id)
    
    # Total tickets sold
    tickets_sold = Ticket.objects.filter(ticket_type__event=event).count()
    
    # Total tickets available
    total_tickets = TicketType.objects.filter(event=event).aggregate(total=Sum('quantity'))['total'] or 0
    tickets_available = total_tickets - tickets_sold
    
    # Validated tickets
    validated_tickets = Ticket.objects.filter(ticket_type__event=event, is_validated=True).count()
    not_validated_tickets = tickets_sold - validated_tickets
    
    # Data for charts
    tickets_by_type = Ticket.objects.filter(ticket_type__event=event).values('ticket_type__name').annotate(count=Count('id'))
    
    # Revenue by ticket type
    revenue_by_ticket_type = Ticket.objects.filter(ticket_type__event=event).values('ticket_type__name').annotate(
        revenue=Sum(F('ticket_type__price'))
    ).order_by('-revenue')
    
    context = {
        'event': event,
        'tickets_sold': tickets_sold,
        'tickets_available': tickets_available,
        'total_tickets': total_tickets,
        'validated_tickets': validated_tickets,
        'not_validated_tickets': not_validated_tickets,
        'tickets_by_type': tickets_by_type,
        'revenue_by_ticket_type': revenue_by_ticket_type,
    }
    return render(request, 'dashboard/event_statistics.html', context)

def is_attendee(user):
    return user.is_authenticated and user.userprofile.role == 'attendee'

@login_required
@user_passes_test(is_attendee)
def attendee_event_dashboard_view(request, event_id):
    event = get_object_or_404(Event, id=event_id, assistants=request.user)
    
    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        try:
            ticket = Ticket.objects.get(id=ticket_id, ticket_type__event=event)
            if not ticket.is_validated:
                ticket.is_validated = True
                ticket.save()
                messages.success(request, f'Ticket {ticket.id} validado exitosamente.')
            else:
                messages.warning(request, f'El ticket {ticket.id} ya ha sido validado.')
        except Ticket.DoesNotExist:
            messages.error(request, 'El ID del ticket no es válido para este evento.')
        return redirect('dashboard:attendee-event-dashboard', event_id=event.id)

    tickets_sold = Ticket.objects.filter(ticket_type__event=event).count()
    validated_tickets = Ticket.objects.filter(ticket_type__event=event, is_validated=True).count()
    
    context = {
        'event': event,
        'tickets_sold': tickets_sold,
        'validated_tickets': validated_tickets,
    }
    return render(request, 'dashboard/attendee_event_dashboard.html', context)
