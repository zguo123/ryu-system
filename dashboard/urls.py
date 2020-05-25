from django.urls import path, re_path
from .views import *

app_name = 'main'
urlpatterns = [
   path('', IndexView.as_view(), name='index'),
   re_path(r'progress/(?P<p_client>\d+)', view_progress, name='view_progress')

]
