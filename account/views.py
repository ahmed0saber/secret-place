from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from .models import Message,Profile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def Logout(request):
    logout(request)
    return redirect('home')

def home(request):
    user = request.user
    if user.is_authenticated:
        messages_box = user.Profile.message_set.all()
        return render(request, 'profile.html', {'messages_box': messages_box})
    return render(request, 'home.html')


def Register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')

        if User.objects.filter(username=username).first():
            messages.success(request, 'Username is taken.')
            return redirect('register')

        user_obj = User(username=username ,first_name=first_name,last_name=last_name ,email=email)
        user_obj.set_password(password1)
        if password1 == password2:
            user_obj.save()
        profile_obj = Profile.objects.create(user=user_obj,username=username,first_name=first_name,last_name=last_name,email=email)
        profile_obj.save()
        return redirect('login')
    return render(request,'register.html')


def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username).first()
        Profile.objects.filter(user=user_obj).first()
        user = authenticate(username=username, password=password)
        if user_obj is None:
            messages.success(request, 'User not found.')
        else:
            login(request,user)
            return redirect('home')
    return render(request,'login.html')


def Profile_User(request, pk):
    profile = User.objects.get(id=pk).Profile
    if profile == request.user.Profile:
        return redirect('home')
    if request.method == 'POST':
        text = request.POST.get('text')
        Message.objects.create(text=text,user=profile)
    return render(request, 'send.html', {"profile":profile})

@login_required(login_url='login')
def setting(request):
    profile = request.user.Profile
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        profile.user.email = email
        profile.user.first_name = first_name
        profile.user.last_name = last_name
        profile.user.save()
    return render(request,'settings.html')




