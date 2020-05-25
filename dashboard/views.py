from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View

from dashboard.progress.project_handlers import get_project
from dashboard.requests.dashboard_requests import get_request


class IndexView(View):
    """
    Main view
    """
    template_name = 'dashboard/pages/dashboard.html'

    def get(self, request, *args, **kwargs):
        """
        Processes the get request for the main page.
        """
        if not request.user.is_authenticated:
            return redirect('auth:login')
        if request.user.is_superuser:
            return redirect('controller:index')
        return render(request, self.template_name, get_request(request))


def view_progress(request, p_client):
    """
    View progress view
    """

    # if request.user.is_superuser:
    #     return redirect(reverse('controller:update_progress', args=[project_client]))

    context = {
        'title': 'RYU | Project Details',
        'project': get_project(p_client)

    }

    return render(request, 'dashboard/pages/progress-view.html', context)
