from django.shortcuts import render
from .models import Schedule
from django.contrib.auth.decorators import login_required

# schedule list page
@login_required(login_url='/accounts/login/')
def schedule_list(request):
    schedules = Schedule.objects.all().order_by('date')
    print(schedules)
    return render(request, 'schedules/schedule_list.html', {'schedules': schedules})
