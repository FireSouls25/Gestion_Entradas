from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)

class TicketType(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    event: "Event"
    
    def __str__(self):
        return f'{self.name} ({self.event.title})'
