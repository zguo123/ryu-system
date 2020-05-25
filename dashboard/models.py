from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    """
    A single project object
    """
    # requested user
    request_user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)

    date_requested = models.DateTimeField()

    estimated_date_of_completion = models.DateTimeField(blank=True, null=True)

    milestones = models.ManyToManyField('Milestone', related_name='project_milestones', blank=True)

    project_name = models.CharField(max_length=10000)

    def __str__(self):
        """
        the string representation of this model
        """
        return f'{self.project_name} requested by: {self.request_user.username}'


class Milestone(models.Model):
    """
    Milestone
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    milestone_name = models.CharField(max_length=1000)
    features = models.ManyToManyField('Feature', related_name='features', blank=True)

    def __str__(self):
        """
        the string representation of this model
        """
        return f'{self.milestone_name} is a part of: {self.project.project_name}'


class Feature(models.Model):
    """
    Feature
    """
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE)
    feature_name = models.CharField(max_length=1000)
    completed = models.BooleanField(default=False)

    def __str__(self):
        """
        the string representation of this model
        """
        return f'{self.feature_name} is a part of: {self.milestone.milestone_name}'
