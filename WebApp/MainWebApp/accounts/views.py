from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your views here.
def signup_view(request):
    if (request.method == 'POST'):
        print(request.POST['email'])
        user = User.objects.create_user(request.POST['email'],request.POST['email'],request.POST['pass']);
        user.save()
        return HttpResponse('signup')
    return render(request, 'accounts/signup.html')

def login_view(request):
    if (request.method == 'POST'):
        print(request.POST['pass'])
        return HttpResponse('login')
    return render(request, 'accounts/login.html')
