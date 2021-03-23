from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.

def login(request):
    if request.user.is_authenticated:
        return redirect('weather:home')
    context = {}
    message = ""
    next = request.GET.get('next')
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']
        user = None
        if User.objects.filter(username=login).exists(): user = auth.authenticate(request, username=login, password=password)
        elif User.objects.filter(email=login).exists():
            login = User.objects.get(email=login).username
            user = auth.authenticate(request, username=login, password=password)
        if user:
            auth.login(request, user)
            if next != "None": return redirect(next)
            else: return redirect("weather:home")
        else: message = "Please fill in all fields correctly!"
    context = {'next':request.GET.get('next'), 'message':message}
    return render(request, 'account/login.html', context)


def signup(request):
    if request.user.is_authenticated:
        return redirect('weather:home')
    message = ""
    next = request.GET.get("next")
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        if username and email and request.POST['password']:
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                message = "Username or email isn't available please try another"
            else:
                user = User.objects.create(username=username,  email=email)
                user.set_password(request.POST['password'])
                user.save()

                auth.login(request, user)
                if next != "None": return redirect(next)
                else: return redirect("weather:home")
    context = {'message':message, 'next':request.GET.get('next')}
    return render(request, 'account/signup.html', context)

    
def logout(request):
    auth.logout(request)
    return redirect("weather:home")
