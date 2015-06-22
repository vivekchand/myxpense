import json
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.http import HttpResponseRedirect, HttpResponse

from .core import get_user, redirect_to_app_if_loggedn, login_required
from myxpense import expense_interactors
from myxpense.models import UserProfile
from myxpense import utils

@redirect_to_app_if_loggedn
def index(request):
    return render(request, 'register.html')


@redirect_to_app_if_loggedn
def login(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')
        user = get_user(username_or_email)
        if user and authenticate(username=user.username, password=password):
            user = authenticate(username=user.username, password=password)
            django_login(request, user)
            return HttpResponseRedirect('/app/#/')
        else:
            return render(request, 'login.html', {'invalid': True})
    else:
        return render(request, 'login.html')


def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/login')


@redirect_to_app_if_loggedn
def signup(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    if not (get_user(email) or get_user(username)):
        user = User.objects.create(
            username=username, email=email, is_active=True)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, parent=user)
        user = authenticate(username=user.username, password=password)
        django_login(request, user)
        return HttpResponseRedirect('/app/#/')
    else:
        return render(request, 'register.html', {'not_available': True})


@login_required
def app(request):
    json_dict = {'expense_books': request.user.expense_books}
    return render(request, 'app.html', json_dict)

