from django.contrib import admin
from django.urls import path, re_path
from . import views

app_name = 'swarm'

urlpatterns = [
    re_path(r'^$',  views.swarm_interface_view, name="swarm_interface"),
]