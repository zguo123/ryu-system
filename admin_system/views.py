# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from dashboard.forms import *
from dashboard.progress.project_handlers import *
from .requests.dashboard_requests import get_request


class IndexView(View):
    """
    Main view
    """
    template_name = 'admin_sys/pages/index.html'

    def get(self, request, *args, **kwargs):
        """
        Processes the get request for the main page.
        """
        if not request.user.is_authenticated:
            return redirect('auth:login')
        else:
            return render(request, self.template_name, get_request(request))


def create_project(request):
    """
    Logic for creating a project
    """
    if request.method == 'POST' and request.is_ajax():
        form = ProjectCreationForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.request_user = User.objects.get(id=form.cleaned_data['requesting_user'])
            project.project_name = form.cleaned_data['project_name'].strip()
            project.date_requested = timezone.now()
            project.save()
            data = {
                'message': "Successfully created project."
            }
            return JsonResponse(data)
        else:
            return JsonResponse(form.errors, status=400)


def progress(request, project_admin):
    """
     Progress view
    """

    context = {
        'title': 'RYU | Progress Admin',
        'project': get_project(project_admin)
    }

    return render(request, 'admin_sys/pages/progress.html', context)


def new_milestone(request):
    """
    Creating a new milestone
    """
    if request.method == 'POST' and request.is_ajax():
        name, project, features = request.POST.get('name'), request.POST.get('project'), request.POST.getlist(
            'features[]')
        milestone = Milestone.objects.create(
            milestone_name=name,
            project=get_project(project),
        )
        for feature in features:
            feature_model = Feature.objects.create(
                milestone=milestone,
                feature_name=feature
            )
            feature_model.save()

            milestone.features.add(feature_model)

        milestone.save()
        get_project(project).milestones.add(milestone)
        get_project(project).save()

    return JsonResponse({})


def mark_feature_as_complete(request, feature_id):
    """
    Marks the feature with <feature_id> as completed
    """
    if request.method == "POST" and request.is_ajax():
        feature = Feature.objects.get(id=feature_id)
        feature.completed = True
        feature.save()
        return JsonResponse({})


def delete_feature(request, feature_id):
    """
    Deletes the feature with <feature_id>
    """
    if request.method == "POST" and request.is_ajax():
        feature = Feature.objects.get(id=feature_id)
        feature.delete()
        return JsonResponse({})


def delete_milestone(request, milestone_id):
    """
    Deletes a milestone with <milestone_id>
    """
    if request.method == "POST" and request.is_ajax():
        milestone = Milestone.objects.get(id=milestone_id)
        milestone.delete()
        return JsonResponse({})


def add_feature(request, milestone_id):
    """
    Adds features to a milestone with <milestone_id>
    """

    if request.method == "POST" and request.is_ajax():
        milestone = Milestone.objects.get(id=milestone_id)
        features = request.POST.getlist('features[]')
        for feature in features:
            feature_model = Feature.objects.create(
                milestone=milestone,
                feature_name=feature
            )
            feature_model.save()

            milestone.features.add(feature_model)

        return JsonResponse({})


def update_date(request, project_id):
    """
    Updates the date of completion (estimated) with <project_id>
    """
    if request.method == "POST" and request.is_ajax():
        project = Project.objects.get(id=project_id)
        date = request.POST.get('date')
        project.estimated_date_of_completion = date
        project.save()

        return JsonResponse({})
