from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from .forms import UserRegisterForm, UserLoginForm, UserEditForm, ProfileEditForm
from .decorators import unauthorised_user
from .models import Profile
from django.contrib.auth.models import User

@unauthorised_user
def user_register(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user) # extend user model
            messages.success(request, 'Account created successfully')
            return redirect(reverse('user-login'))
    context = {'form': form}
    return render(request, 'register.html', context)


@unauthorised_user
def user_login(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )
            if user:
                login(request, user)
                messages.success(request, f'welcome back {user.username}')
                return redirect('task-list')
            messages.info(request, 'Incorrect credential')
    context = {'form': form}
    return render(request, 'login.html', context)


@login_required(login_url='user-login')
def user_logout(request):
    logout(request)
    return redirect('user-login')


@login_required(login_url='user-login')
def user_profile(request):
    old_profile_path = request.user.profile.image.path
    user_form = UserEditForm(instance=request.user)
    profile_form = ProfileEditForm(instance=request.user.profile)
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            Profile.remove_old_img(request, old_profile_path)
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated')
            return redirect('user-profile')
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'profile.html', context)

