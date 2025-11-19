from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
import pandas as pd
from tickets.models import Ticket
from events.models import Event, TicketType
from django.db.models import Count, Sum, F
import io
import xlsxwriter

def is_organizer(user):
    return user.is_authenticated and user.userprofile.role == 'organizer'

@user_passes_test(is_organizer)
def export_attendees_to_excel(request, event_id):
    event = Event.objects.get(id=event_id)
    
    # Fetch data for Attendees
    tickets = Ticket.objects.filter(ticket_type__event=event)
    attendees_data = {
        'Asistente': [ticket.attendee.username for ticket in tickets],
        'Tipo de Entrada': [ticket.ticket_type.name for ticket in tickets],
        'Fecha de Compra': [ticket.purchase_time.strftime('%Y-%m-%d %H:%M:%S') for ticket in tickets],
        'Validada': ['Sí' if ticket.is_validated else 'No' for ticket in tickets],
    }
    df_attendees = pd.DataFrame(attendees_data)

    # Fetch data for Tickets Sold vs. Available
    tickets_sold = tickets.count()
    total_tickets_available = TicketType.objects.filter(event=event).aggregate(total=Sum('quantity'))['total'] or 0
    tickets_available = total_tickets_available - tickets_sold
    df_tickets_sold_available = pd.DataFrame({
        'Estado': ['Vendidos', 'Disponibles'],
        'Cantidad': [tickets_sold, tickets_available]
    })

    # Fetch data for Tickets Validated vs. Not Validated
    validated_tickets = tickets.filter(is_validated=True).count()
    not_validated_tickets = tickets_sold - validated_tickets
    df_tickets_validated = pd.DataFrame({
        'Estado': ['Validados', 'No Validados'],
        'Cantidad': [validated_tickets, not_validated_tickets]
    })

    # Fetch data for Revenue by Ticket Type
    revenue_by_ticket_type = Ticket.objects.filter(ticket_type__event=event).values('ticket_type__name').annotate(
        revenue=Sum(F('ticket_type__price'))
    ).order_by('-revenue')
    df_revenue = pd.DataFrame(list(revenue_by_ticket_type))
    df_revenue.rename(columns={'ticket_type__name': 'Tipo de Entrada', 'revenue': 'Ingresos'}, inplace=True)

    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    workbook = writer.book

    # Sheet 1: Attendees
    df_attendees.to_excel(writer, sheet_name='Asistentes', index=False, startrow=1, header=False)
    worksheet_attendees = writer.sheets['Asistentes']

    # Add header format
    header_format = workbook.add_format({
        'bg_color': '#800080',  # Purple
        'font_color': '#FFFFFF', # White
        'bold': True,
        'border': 1
    })
    for col_num, value in enumerate(df_attendees.columns.values):
        worksheet_attendees.write(0, col_num, value, header_format)
    
    # Add row formatting
    even_row_format = workbook.add_format({'bg_color': '#F2F2F2', 'border': 1})
    odd_row_format = workbook.add_format({'border': 1})
    for row_num, row_data in enumerate(df_attendees.values):
        fmt = even_row_format if (row_num % 2 == 0) else odd_row_format
        for col_num, value in enumerate(row_data):
            worksheet_attendees.write(row_num + 1, col_num, value, fmt)
    worksheet_attendees.set_column(0, len(df_attendees.columns) - 1, 20) # Adjust column width

    # Sheet 2: Tickets Sold vs. Available
    df_tickets_sold_available.to_excel(writer, sheet_name='Tickets Vendidos', index=False, startrow=1, header=False)
    worksheet_sold = writer.sheets['Tickets Vendidos']
    for col_num, value in enumerate(df_tickets_sold_available.columns.values):
        worksheet_sold.write(0, col_num, value, header_format)
    for row_num, row_data in enumerate(df_tickets_sold_available.values):
        fmt = even_row_format if (row_num % 2 == 0) else odd_row_format
        for col_num, value in enumerate(row_data):
            worksheet_sold.write(row_num + 1, col_num, value, fmt)
    worksheet_sold.set_column(0, len(df_tickets_sold_available.columns) - 1, 20)

    # Create a new chart object.
    chart_sold = workbook.add_chart({'type': 'pie'})
    chart_sold.add_series({
        'name':       'Tickets Vendidos vs. Disponibles',
        'categories': ['Tickets Vendidos', 1, 0, df_tickets_sold_available.shape[0], 0],
        'values':     ['Tickets Vendidos', 1, 1, df_tickets_sold_available.shape[0], 1],
        'points': [
            {'fill': {'color': '#800080'}},
            {'fill': {'color': '#D3D3D3'}},
        ],
    })
    chart_sold.set_title({'name': 'Tickets Vendidos vs. Disponibles'})
    chart_sold.set_style(10)
    worksheet_sold.insert_chart('D2', chart_sold, {'x_offset': 25, 'y_offset': 10})

    # Sheet 3: Tickets Validated
    df_tickets_validated.to_excel(writer, sheet_name='Tickets Validados', index=False, startrow=1, header=False)
    worksheet_validated = writer.sheets['Tickets Validados']
    for col_num, value in enumerate(df_tickets_validated.columns.values):
        worksheet_validated.write(0, col_num, value, header_format)
    for row_num, row_data in enumerate(df_tickets_validated.values):
        fmt = even_row_format if (row_num % 2 == 0) else odd_row_format
        for col_num, value in enumerate(row_data):
            worksheet_validated.write(row_num + 1, col_num, value, fmt)
    worksheet_validated.set_column(0, len(df_tickets_validated.columns) - 1, 20)

    chart_validated = workbook.add_chart({'type': 'doughnut'})
    chart_validated.add_series({
        'name':       'Tickets Validados vs. No Validados',
        'categories': ['Tickets Validados', 1, 0, df_tickets_validated.shape[0], 0],
        'values':     ['Tickets Validados', 1, 1, df_tickets_validated.shape[0], 1],
        'points': [
            {'fill': {'color': '#4BC0C0'}},
            {'fill': {'color': '#FF6384'}},
        ],
    })
    chart_validated.set_title({'name': 'Tickets Validados'})
    chart_validated.set_style(10)
    worksheet_validated.insert_chart('D2', chart_validated, {'x_offset': 25, 'y_offset': 10})

    # Sheet 4: Revenue by Ticket Type
    df_revenue.to_excel(writer, sheet_name='Ingresos por Tipo', index=False, startrow=1, header=False)
    worksheet_revenue = writer.sheets['Ingresos por Tipo']
    for col_num, value in enumerate(df_revenue.columns.values):
        worksheet_revenue.write(0, col_num, value, header_format)
    for row_num, row_data in enumerate(df_revenue.values):
        fmt = even_row_format if (row_num % 2 == 0) else odd_row_format
        for col_num, value in enumerate(row_data):
            worksheet_revenue.write(row_num + 1, col_num, value, fmt)
    worksheet_revenue.set_column(0, len(df_revenue.columns) - 1, 20)

    chart_revenue = workbook.add_chart({'type': 'column'})
    chart_revenue.add_series({
        'name':       'Ingresos',
        'categories': ['Ingresos por Tipo', 1, 0, df_revenue.shape[0], 0],
        'values':     ['Ingresos por Tipo', 1, 1, df_revenue.shape[0], 1],
        'fill':       {'color': '#9966FF'},
        'border':     {'color': '#9966FF'},
    })
    chart_revenue.set_title({'name': 'Ingresos por Tipo de Ticket'})
    chart_revenue.set_x_axis({'name': 'Tipo de Entrada'})
    chart_revenue.set_y_axis({'name': 'Ingresos'})
    chart_revenue.set_style(10)
    worksheet_revenue.insert_chart('D2', chart_revenue, {'x_offset': 25, 'y_offset': 10})

    writer.close()
    workbook.close()
    output.seek(0)

    response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=reporte_evento_{event.title}.xlsx'
    return response