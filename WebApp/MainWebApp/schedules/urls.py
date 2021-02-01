from django.urls import path, re_path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

app_name = 'schedules'

urlpatterns = [
    re_path(r'^$', views.schedule_list, name='schedules'),
]

# adding static locations for the debug purpose
urlpatterns += staticfiles_urlpatterns()