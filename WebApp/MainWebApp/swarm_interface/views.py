from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/accounts/login/')
def swarm_interface_view(request):
    return render(request, 'swarm_interface/index.html')
    return HttpResponse('swarm interface')