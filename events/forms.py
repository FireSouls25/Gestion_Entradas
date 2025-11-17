from django import forms
from .models import Event, Location

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time', 'location']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'address', 'capacity']