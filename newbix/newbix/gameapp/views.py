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


def not_authenticated(user):
    return not user.is_authenticated


def index(request):
    return render(request, 'gameapp/index.html')


@user_passes_test(not_authenticated, login_url='/gameapp/profile_page')
def login_page(request):
    return render(request, 'gameapp/login_page.html')


@user_passes_test(not_authenticated, login_url='/gameapp/profile_page')
def login_load(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('votacao:index'))
    else:
        return render(request, 'votacao/loginPage.html', {'error_message': "Este utilizador não existe."})


@user_passes_test(not_authenticated, login_url='/gameapp/profile_page')
def signin_page(request):
    return render(request, 'gameapp/signin_page.html')


@user_passes_test(not_authenticated, login_url='/gameapp/profile_page')
def signin_load(request):
    return None


@login_required(login_url='/gameapp/login_page')
def profile_page(request):
    return render(request, 'gameapp/profile_page.html')
