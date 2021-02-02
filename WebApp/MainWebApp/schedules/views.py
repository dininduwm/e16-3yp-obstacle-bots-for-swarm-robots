from django.shortcuts import render, redirect, HttpResponse
from .models import Schedule, AuthorizeClient
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
@login_required(login_url='/accounts/login/')
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
        query = AuthorizeClient.objects.filter(user=request.user)
        if len(query) > 0:            
            if not query[0].auth_stat:
                return render(request, 'schedules/unauthorized.html')
        else:
            return render(request, 'schedules/unauthorized.html')
        form = forms.CreateSchedule()
    return render(request, 'schedules/schedule_create.html', {'form': form})
