from django import forms
from . import models

class CreateSchedule(forms.ModelForm):
    class Meta:
        model = models.Schedule
        fields = ['project_name', 'description', 'server_id']