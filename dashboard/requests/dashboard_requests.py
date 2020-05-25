from dashboard.models import Project


def get_request(request):

    return {
        'dashboard': 'active',
        'title': 'RYU | Client Home',
        'projects': Project.objects.filter(request_user=request.user)
    }