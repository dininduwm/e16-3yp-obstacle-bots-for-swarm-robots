from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout

# Create your views here.
def home_view(request):
    # return HttpResponse("Test")
    return render(request, 'homepage.html')
