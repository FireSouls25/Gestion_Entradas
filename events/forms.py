from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Sum
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

    def clean(self):
        cleaned_data = super().clean()
        location = cleaned_data.get('location')
        
        if location:
            # For existing events, sum up existing ticket quantities
            if self.instance.pk:
                existing_tickets_quantity = TicketType.objects.filter(event=self.instance).aggregate(total_quantity=forms.Sum('quantity'))['total_quantity'] or 0
            else:
                existing_tickets_quantity = 0

            # Check if the location's capacity is sufficient
            if location.capacity < existing_tickets_quantity:
                raise ValidationError(
                    f'La capacidad de la ubicación ({location.capacity}) es menor que la cantidad de entradas ya creadas ({existing_tickets_quantity}).'
                )
        return cleaned_data
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