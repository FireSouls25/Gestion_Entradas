from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Event, Location
from .forms import EventForm, LocationForm
from tickets.models import Ticket

class OrganizerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.userprofile.role == 'organizer'

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                ticket = Ticket.objects.get(
                    attendee=self.request.user,
                    ticket_type__event=self.object
                )
                context['user_ticket'] = ticket
            except Ticket.DoesNotExist:
                context['user_ticket'] = None
        return context

class EventCreateView(LoginRequiredMixin, OrganizerRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:event-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['locations'] = Location.objects.all()
        return context

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, OrganizerRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:event-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['locations'] = Location.objects.all()
        return context

class EventDeleteView(LoginRequiredMixin, OrganizerRequiredMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('events:event-list')

# Location CRUD Views
class LocationListView(LoginRequiredMixin, OrganizerRequiredMixin, ListView):
    model = Location
    template_name = 'events/location_list.html'
    context_object_name = 'locations'

class LocationCreateView(LoginRequiredMixin, OrganizerRequiredMixin, CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'events/location_form.html'
    success_url = reverse_lazy('events:location-list')

class LocationUpdateView(LoginRequiredMixin, OrganizerRequiredMixin, UpdateView):
    model = Location
    form_class = LocationForm
    template_name = 'events/location_form.html'
    success_url = reverse_lazy('events:location-list')

class LocationDeleteView(LoginRequiredMixin, OrganizerRequiredMixin, DeleteView):
    model = Location
    template_name = 'events/location_confirm_delete.html'
    success_url = reverse_lazy('events:location-list')
