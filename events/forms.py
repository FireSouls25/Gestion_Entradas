from django import forms
from .models import Event, Location, TicketType

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time', 'location']
        labels = {
            'title': 'Título',
            'description': 'Descripción',
            'start_time': 'Hora de Inicio',
            'end_time': 'Hora de Fin',
            'location': 'Ubicación',
        }
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'address', 'capacity']
        labels = {
            'name': 'Nombre',
            'address': 'Dirección',
            'capacity': 'Capacidad',
        }

class TicketTypeForm(forms.ModelForm):
    class Meta:
        model = TicketType
        fields = ['name', 'price', 'quantity']
        labels = {
            'name': 'Nombre',
            'price': 'Precio',
            'quantity': 'Cantidad',
        }

class TicketPurchaseForm(forms.Form):
    ticket_type = forms.ModelChoiceField(queryset=TicketType.objects.all(), empty_label="Selecciona un tipo de entrada", label="Tipo de Entrada")
    quantity = forms.IntegerField(min_value=1, initial=1, label="Cantidad")