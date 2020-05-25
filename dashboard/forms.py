from django import forms
from django.forms import Select

from .models import *


class ProjectCreationForm(forms.ModelForm):
    """
    Form for creating a new project
    """

    requesting_user = forms.ChoiceField(
        choices=[(u.id, u.username) for u in User.objects.filter(is_superuser=False).all()]
    )

    project_name = forms.CharField(
        widget=forms.TextInput()
    )

    class Meta:
        model = Project
        fields = ('requesting_user','project_name')
        widgets = {
            'users': Select(attrs={'class': 'select'})
        }
