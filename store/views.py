from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import login

from store.forms import LoginForm, RegisterForm, CreateGameForm
from store.models import Game, Purchase


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
                    return HttpResponseRedirect('../developer')
                elif user.groups.filter(name='player'):
                    return HttpResponseRedirect('../player')
            else:
                return render(request, 'login.html', {'form': form,'msg':'Username or password is not correct!','can_not_login': True})
        else:
            return render(request, 'login.html', {'form': form, 'msg': 'Username or password is not correct!','can_not_login': True})
    form = LoginForm()
    return render(request, 'login.html', {'form': form, 'can_not_login': False})

def player_play_game(request, game_name):
    return HttpResponse('This is test player, playing game' + str(game_name))

def player_list_games(request):
    return HttpResponse('This is game list of test player')


def developer_modify_game(request, game_name):
    game = Game.objects.get(game_name=game_name)
    if game.developer != request.user:
        return HttpResponseRedirect('login', {'msg':'You don\' t have the access to this game'})
    form = CreateGameForm(initial={'game_url':game.url, 'game_name':game.game_name, 'game_price': game.price})
    return render(request, 'create_game.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid() and form.cleaned_data['password'] == form.cleaned_data['password_confirm']:
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            group_name = form.cleaned_data['role']
            group = Group.objects.get(name=group_name)
            try:
                user = User.objects.create_user(username,email,password)
                group.user_set.add(user)
                return HttpResponseRedirect('../login')
            except IntegrityError:
                return render(request, 'register.html', {'form': form, 'error': 'Username already exists'})

        else:
            return render(request, 'register.html', {'form':form, 'error': 'Please check your username and password if they meet requirements.'})
    form = RegisterForm()
    return render(request,'register.html', {'form':form,'error':''})

@login_required(login_url='login')
def developer_main(request):
    user = request.user
    if len(user.groups.filter(name='player')) > 0:
        return HttpResponseRedirect('player_main')
    game_list = Game.objects.filter(developer=user)

    #return HttpResponse('This is test developer main' + str(request.user))
    return render(request,'developer_main.html', {'games':game_list})

@login_required(login_url='login')
def player_main(request):
    user = request.user
    if len(user.groups.filter(name='dev')) > 0:
        print("Not player")
        return HttpResponseRedirect('developer_main')
    purchase_history = Purchase.objects.filter(user=user)
    return HttpResponse('This is test player main' + str(user))

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('login')

@login_required(login_url='login')
def developer_create_game(request):
    user = request.user
    if request.method == 'POST':
        form = CreateGameForm(request.POST)
        if form.is_valid():
            game_name = form.cleaned_data['game_name']
            price = form.cleaned_data['game_price']
            url = form.cleaned_data['game_url']
            if len(Game.objects.filter(game_name=game_name)) > 0:
                print('Game already exists')
                return render(request, "create_game.html", {'form': form, 'msg':'Game already exists'})
            else:
                g = Game(game_name=game_name, price=price, developer=user, copies_sold=0, url=url)
                g.save()
                return render(request, "create_game.html", {'form': form, 'msg': 'Game created'})
        else:
            return render(request, "create_game.html", {'form': form, 'msg': 'Illegal input'})
    form = CreateGameForm()
    return render(request, "create_game.html", {'form': form})

@login_required(login_url='login')
def developer_game_buyer(request, game_id):
    #list all purchase history of a game
   pass

