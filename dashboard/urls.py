from django.urls import path
from .views import dashboard_view, event_statistics_view

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('event/<int:event_id>/statistics/', event_statistics_view, name='event-statistics'),
]
