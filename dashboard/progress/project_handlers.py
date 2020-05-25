"""
This file is to handle all the project requests
"""
from dashboard.models import *


def get_project(pid):
    """
    Gets the project with <pid>
    """
    return Project.objects.get(id=pid)


def get_milestones(project_id):
    """
    This function is to get all the milestones for this project
    with <project_id>
    """
    return Milestone.objects.filter(project=project_id).all()


def get_features(milestone_id):
    """
    Gets the features associated with milestone with <milestone_id>
    """
    return Feature.objects.filter(milestone=milestone_id).all()
