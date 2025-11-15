from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    try:
        role = request.user.userprofile.role
        if role == 'organizer':
            return render(request, 'dashboard/dashboard_organizer.html')
        elif role == 'attendee':
            return render(request, 'dashboard/dashboard_attendee.html')
    except AttributeError:
        # Handle cases where userprofile might not exist
        return render(request, 'dashboard.html')
    return render(request, 'dashboard.html')
