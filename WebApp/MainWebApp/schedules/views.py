from django.shortcuts import render, redirect
from .models import Schedule
from django.contrib.auth.decorators import login_required
from . import forms

# schedule list page
@login_required(login_url='/accounts/login/')
def schedule_list(request):
    schedules = Schedule.objects.all().order_by('date')
    # give autherization to control the reobot
    allowControl = False
    if len(schedules) > 0:
        if schedules[0].user == request.user:
            print("Its me")
            allowControl = True
    return render(request, 'schedules/schedule_list.html', {'schedules': schedules, 'control': allowControl})

# schedule create page
@login_required(login_url='/accounts/create/')
def schedule_create(request):
    if request.method == 'POST':
        form = forms.CreateSchedule(request.POST)
        if form.is_valid():
            # saving articles
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('schedules:list')
    else:
        form = forms.CreateSchedule()
    return render(request, 'schedules/schedule_create.html', {'form': form})
