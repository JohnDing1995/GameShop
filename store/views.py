from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
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
            group = form.cleaned_data['role']
            user = authenticate(username=username, password=password, group=group)
            if user is not None:
                login(request, user)
                if group is 'dev':
                    return HttpResponseRedirect(reverse('dev_main'))
                else:
                    return HttpResponseRedirect(reverse('player_main'))
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
    form = RegisterForm()
    return render(request, 'register.html', {'form':form,'error':''})