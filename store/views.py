import uuid
from hashlib import md5
import requests
import json

from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import login
from django.urls import reverse

from store.forms import LoginForm, RegisterForm, CreateGameForm
from store.models import Game, Purchase, Score
from store.utilities import pay

ERROR_MSG = "{messageType: \"ERROR\",info: \"Gamestate could not be loaded\"};"


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # request.session['name'] = username
                # request.session['pwd'] = password
                if user.groups.filter(name='dev').exists():
                    return HttpResponseRedirect('../developer')
                elif user.groups.filter(name='player'):
                    return HttpResponseRedirect('../player')
            else:
                return render(request, 'login.html',
                              {'form': form, 'msg': 'Username or password is not correct!', 'can_not_login': True})
        else:
            return render(request, 'login.html',
                          {'form': form, 'msg': 'Username or password is not correct!', 'can_not_login': True})
    form = LoginForm()
    return render(request, 'login.html', {'form': form, 'can_not_login': False})


def player_play_game(request, game_name):
    game = Game.objects.get(game_name=game_name)

    scores = Score.objects.filter(game=game)
    highscores = scores.order_by('score').reverse()[:3]

    return render(request, 'play.html', {'game': game, 'highscores': highscores})


def developer_modify_game(request, game_name):
    game = Game.objects.get(game_name=game_name)
    if game.developer != request.user:
        return redirect('/login', {'msg': 'You don\' t have the access to this game'})
    if request.method == 'POST':
        form = CreateGameForm(request.POST)
        if form.is_valid():
            game.game_name = form.cleaned_data['game_name']
            game.price = form.cleaned_data['game_price']
            game.url = form.cleaned_data['game_url']
            game.save()
            return render(request, 'create_game.html', {'form': form, 'msg': 'Game successfully updated'})
        else:
            return render(request, 'create_game.html', {'form': form, 'msg': 'Form error'})

    form = CreateGameForm(initial={'game_url': game.url, 'game_name': game.game_name, 'game_price': game.price})
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
                user = User.objects.create_user(username, email, password)
                group.user_set.add(user)
                return HttpResponseRedirect('../login')
            except IntegrityError:
                return render(request, 'register.html', {'form': form, 'error': 'Username already exists'})

        else:
            return render(request, 'register.html',
                          {'form': form, 'error': 'Please check your username and password if they meet requirements.'})
    form = RegisterForm()
    return render(request, 'register.html', {'form': form, 'error': ''})


@login_required(login_url='/login')
def developer_main(request):
    user = request.user
    if len(user.groups.filter(name='player')) > 0:
        return redirect('player_main')
    game_list = Game.objects.filter(developer=user)

    # return HttpResponse('This is test developer main' + str(request.user))
    return render(request, 'developer_main.html', {'games': game_list})


@login_required(login_url='/login')
def player_main(request):
    user = request.user
    if len(user.groups.filter(name='dev')) > 0:
        print("Not player")
        return redirect('developer_main')
    purchase_history = Purchase.objects.filter(user=user, result=True)
    return render(request, 'player_main.html', {'purchase_history': purchase_history})


@login_required(login_url='/login')
def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required(login_url='/login')
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
                return render(request, "create_game.html", {'form': form, 'msg': 'Game already exists'})
            else:
                g = Game(game_name=game_name, price=price, developer=user, copies_sold=0, url=url)
                g.save()
                return render(request, "create_game.html", {'form': form, 'msg': 'Game created'})
        else:
            return render(request, "create_game.html", {'form': form, 'msg': 'Illegal input'})
    form = CreateGameForm()
    return render(request, "create_game.html", {'form': form})


@login_required(login_url='/login')
def developer_game_buyer(request, game_name):
    # list all purchase history of a game
    user = request.user
    game_history = Purchase.objects.filter(game__game_name=game_name)
    return render(request, "game_sale.html", {'sale': game_history})


@login_required(login_url='/login')
def store(request):
    user = request.user
    if len(user.groups.filter(name='dev')) > 0:
        print("Not player")
        return redirect('developer_main')
    all_games = Game.objects.all()
    return render(request, "store.html", {'games': all_games})


@login_required(login_url='/login')
def player_buy_game(request, game_name):
    user = request.user
    if len(user.groups.filter(name='dev')) > 0:
        print("Not player")
        return redirect('developer_main')
    game = Game.objects.get(game_name=game_name)
    player_own_game = Purchase.objects.filter(user=user, result=True)
    if (len(player_own_game.filter(game=game)) > 0):
        return render(request, "buy_game.html", {'msg': 'You already owned the game ' + game_name, 'owned': True})
    pid = str(uuid.uuid1().hex)
    amount = game.price
    checksum_str = "pid={}&sid={}&amount={}&token={}".format(pid, "plr", amount, "c12ccb024b3d72922f9b85575e76154d")
    success_url = "http://localhost:8000/player/success"
    print(success_url)
    m = md5(checksum_str.encode("ascii"))
    checksum = m.hexdigest()
    post_data = {
        "pid": pid,
        "amount": amount,
        "sid": 'plr',
        "success_url": success_url,
        "cancel_url": "http://localhost:8000/player/store",
        "error_url": "http://localhost:8000/player/store",
        "checksum": checksum,
        "owned": False
    }
    print(post_data)
    # Add a unfinished purchase first
    p = Purchase(game=game, user=user, pid=pid, amount=amount, checksum=checksum, result=False)
    p.save()
    return render(request, "buy_game.html", post_data)


# Will be log out when redirected from payment service to our website
def player_buy_game_success(request):
    pid = request.GET.get('pid')
    p = Purchase.objects.get(pid=pid)
    p.result = True
    game = p.game
    game.copies_sold += 1
    game.save()
    p.save()
    # get user object by pid and re-login
    login(request, p.user)

    return render(request, "buy_game_success.html", {'data':request.GET.dict(), 'game_name':game.game_name})


@login_required()
def player_save_game(request, game_name):
    user = request.user
    if request.method == 'POST':
        print('save')
        game = Game.objects.get(game_name=game_name)
        json_score = request.POST.get('data')
        json_score = json.loads(json_score)
        return JsonResponse({'message': 'Game saved'})


@login_required()
def player_load_game(request, game_name):
    user = request.user


@login_required()
def player_submit_score(request, game_name):
    user = request.user
    if request.method == 'POST':
        print('score')
        game = Game.objects.get(game_name=game_name)
        current_score = request.POST.get('score')
        try:
            record_score = Score.objects.get(game=game, user=user).score
            if record_score < float(current_score):
                new_score = Score.objects.get(game=game, user=user)
                new_score.score = current_score
                new_score.save()
        except ObjectDoesNotExist:
            Score.objects.create(game=game, user=user, score=current_score)

    return JsonResponse({'message': 'Score submitted'})


@login_required(login_url='/login')
def developer_sales(request):
    # list all purchase history of a game
    user = request.user
    game_history = Purchase.objects.filter(game__developer=user)

    return render(request, "game_sale.html", {'sale':game_history})

