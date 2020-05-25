from django.urls import path, re_path

from .views import *

app_name = 'controller'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create_project/', create_project, name='make_project'),
    re_path('update_progress/(?P<project_admin>[0-9]+)', progress, name='update_progress'),
    path('new_milestone/', new_milestone, name='new_milestone'),
    re_path('add_feature/(?P<milestone_id>[0-9]+)', add_feature, name='add_features'),
    re_path('delete_milestone/(?P<milestone_id>[0-9]+)', delete_milestone, name='delete_milestone'),
    re_path('feature_complete/(?P<feature_id>[0-9]+)', mark_feature_as_complete, name='feature_complete'),
    re_path('delete_feature/(?P<feature_id>[0-9]+)', delete_feature, name='delete_feature'),
    re_path('update_date/(?P<project_id>[0-9]+)', update_date, name="update_date")

]
