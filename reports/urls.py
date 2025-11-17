from django.urls import path
from .views import export_attendees_to_excel

app_name = 'reports'

urlpatterns = [
    path('event/<int:event_id>/export/excel/', export_attendees_to_excel, name='export-attendees-excel'),
]
