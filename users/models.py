from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_ROLE_CHOICES = (
        ('organizer', 'Organizer'),
        ('attendee', 'Attendee'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES)

    def __str__(self):
        return f'{self.user.username} - {self.role}'
