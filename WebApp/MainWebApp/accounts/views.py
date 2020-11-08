from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout

# Create your views here.
def signup_view(request):
    if (request.method == 'POST'):
        print(request.POST['email'])
        user = User.objects.create_user(request.POST['email'],request.POST['email'],request.POST['pass']);
        # saving the user
        user.save()
        # loggin in the user
        login(request, user)
        return redirect('home')
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

                # checking the next field is in the redirect
                if 'next' in request.POST:
                    return redirect(request.POST['next'])
                else:
                    return redirect('home')
            else:
                return HttpResponse('invalid user name password combination')
        
    return render(request, 'accounts/login.html')


def logout_view(request):
    if (request.method == 'POST'):
        # loging out the user
        logout(request)
        return redirect('home')
