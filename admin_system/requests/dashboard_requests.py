from dashboard.forms import *


def get_request(request):
    return {
        'dashboard_admin': 'active',
        'title': 'RYU | Admin Home',
        'project_creation': ProjectCreationForm,
        'projects': Project.objects.all()
    }
