from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
User = get_user_model()

from .forms import UserRegisterForm, UserLoginForm, ProfileForm

def login_view(request):
    print(request.user.is_authenticated)
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("/")
    context = {
        'form': form
    }
    return render(request,"login.html",context)

def logout_view(request):
    logout(request)
    return redirect("/")
    return render(request,"login.html",{'form':form})

def register_view(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        # Create an Entry for the new User
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        # Check if the user exist and login
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect("/")

    context = {
        'form': form
    }
    return render(request,'register.html',context)

def profile_view(request):
    form = ProfileForm(request.POST or None)
    context = {
        'form': form
    }
    user_info = {}
    if request.user.is_authenticated == True:
        context['username'] = request.user.get_username()
        if form.is_valid():
            username_qs = User.objects.get(username=context['username'])
            username_qs.username = form.cleaned_data.get('username')
            username_qs.save()
            return redirect("/")
    else:
        return redirect("/register/")
    return render(request,'profile.html',context)
