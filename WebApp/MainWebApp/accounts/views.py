from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login

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
        user = User.objects.filter(username=request.POST['email'])
        # checking for the ecistance of the user
        if (len(user) == 0):
            return HttpResponse('invalid user name')
        else:
            # checking for the password
            if (user[0].check_password(request.POST['pass'])):
                # logging in the user
                login(request, user[0])
                return HttpResponse('successfully loged in')
            else:
                return HttpResponse('invalid user name password combination')
        return HttpResponse('login')
    return render(request, 'accounts/login.html')
