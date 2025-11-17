from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from events.models import Event
from tickets.models import Ticket
from django.db.models import Count

@login_required
def dashboard_view(request):
    try:
        role = request.user.userprofile.role
        if role == 'organizer':
            events = Event.objects.filter(organizer=request.user)
            return render(request, 'dashboard/dashboard_organizer.html', {'events': events})
        elif role == 'attendee':
            return render(request, 'dashboard/dashboard_attendee.html')
        elif role == 'client':
            return render(request, 'dashboard/dashboard_client.html')
    except AttributeError:
        # Handle cases where userprofile might not exist
        return render(request, 'dashboard.html')
    return render(request, 'dashboard.html')

@login_required
def event_statistics_view(request, event_id):
    event = Event.objects.get(id=event_id)
    tickets_sold = Ticket.objects.filter(ticket_type__event=event).count()
    attendees = Ticket.objects.filter(ticket_type__event=event, is_validated=True).count()
    
    # Data for charts
    tickets_by_type = Ticket.objects.filter(ticket_type__event=event).values('ticket_type__name').annotate(count=Count('id'))
    
    context = {
        'event': event,
        'tickets_sold': tickets_sold,
        'attendees': attendees,
        'tickets_by_type': tickets_by_type,
    }
    return render(request, 'dashboard/event_statistics.html', context)
