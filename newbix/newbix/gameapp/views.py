import django.contrib.auth.models
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout

from .models import Utilizador


def not_authenticated(user):
    return not user.is_authenticated


def index(request):
    return render(request, 'gameapp/index.html')


@user_passes_test(not_authenticated, login_url='/gameapp/profile')
def login_page(request):
    return render(request, 'gameapp/login_page.html')


@user_passes_test(not_authenticated, login_url='/gameapp/profile')
def login_load(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('gameapp:index'))
    else:
        return render(request, 'gameapp/login_page.html', {'error_message': "Nome ou Password errados."})


@user_passes_test(not_authenticated, login_url='/gameapp/profile')
def signin_page(request):
    return render(request, 'gameapp/signin_page.html')


@user_passes_test(not_authenticated, login_url='/gameapp/profile')
def signin_load(request):
    username = request.POST['username']
    try:
        if User.objects.get(username=username):
            return render(request, 'gameapp/signin_page.html', {'error_message': "User already exists."})
    except django.contrib.auth.models.User.DoesNotExist:
        _ = None
    password = request.POST['password']
    email = request.POST['email']
    user = User.objects.create_user(username=username, email=email, password=password)
    Utilizador.objects.create(user_id=user)
    login(request, user)
    return index(request)


@login_required(login_url='/gameapp/login')
def profile_page(request):
    return render(request, 'gameapp/profile_page.html')


def logout_load(request):
    logout(request)
    return HttpResponseRedirect(reverse('gameapp:index'))
