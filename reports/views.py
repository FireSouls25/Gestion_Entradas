from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
import pandas as pd
from tickets.models import Ticket
from events.models import Event

def is_organizer(user):
    return user.is_authenticated and user.userprofile.role == 'organizer'

@user_passes_test(is_organizer)
def export_attendees_to_excel(request, event_id):
    event = Event.objects.get(id=event_id)
    tickets = Ticket.objects.filter(ticket_type__event=event)
    
    data = {
        'Asistente': [ticket.attendee.username for ticket in tickets],
        'Tipo de Entrada': [ticket.ticket_type.name for ticket in tickets],
        'Fecha de Compra': [ticket.purchase_time.strftime('%Y-%m-%d %H:%M:%S') for ticket in tickets],
        'Validada': ['Sí' if ticket.is_validated else 'No' for ticket in tickets],
    }
    
    df = pd.DataFrame(data)
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=asistentes_{event.title}.xlsx'
    
    df.to_excel(response, index=False)
    
    return response