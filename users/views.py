from urllib import request

from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm


class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        print(form)
        return render(request, 'templates/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect('accounts:login')
        return render(request, 'templates/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'templates/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect('templates:profile')
        else:

            print(form.errors)
        return render(request, 'templates/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)

        return redirect('users:login')