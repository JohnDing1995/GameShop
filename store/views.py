from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import login

# Create your views here.
from django.urls import reverse

from store import models
from store.forms import LoginForm, RegisterForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.groups.filter(name='dev').exists():
                    return HttpResponseRedirect('../developer/')
                elif user.groups.filter(name='player'):
                    return HttpResponseRedirect('../player/')
            else:
                return render(request, 'login.html', {'form': form,'msg':'Username or password is not correct!','can_not_login': True})
        else:
            return render(request, 'login.html', {'form': form, 'msg': 'Username or password is not correct!','can_not_login': True})
    form = LoginForm()
    return render(request, 'login.html', {'form': form, 'can_not_login': False})

def player_list_games(request):
    return HttpResponse('This is game list of test player')


def player_play_game(request, game_id):
    return HttpResponse('This is test player, playing game' + str(game_id))


def developer_list_games(request):
    return HttpResponse('This is game list of test developer')


def developer_set_game(request, game_id):
    return HttpResponse('This is test developer, setting game' + str(game_id))


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid() and form.cleaned_data['password'] == form.cleaned_data['password_confirm']:
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            group_name = form.cleaned_data['role']
            print(group_name)
            group = Group.objects.get(name=group_name)

            user = User.objects.create_user(username,email,password)
            group.user_set.add(user)
            return HttpResponseRedirect('../login')
        else:
            return render(request, 'register.html', {'form':form, 'error': 'Please check your username and password if they meet requirements.'})
    form = RegisterForm()
    return render(request,'register.html', {'form':form,'error':''})


def developer_main(request):
    return HttpResponse('This is test developer main' + str(request.user))


def player_main(request):
    return HttpResponse('This is test player main' + str(request.user))