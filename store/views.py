import base64
import uuid
from hashlib import md5
import requests
import json

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import login
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlencode, urlsafe_base64_encode, urlsafe_base64_decode

from store.forms import LoginForm, RegisterForm, CreateGameForm
from store.models import Game, Purchase, Score
from store.decorators import developer_required, player_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

ERROR_MSG = "{messageType: \"ERROR\",info: \"Gamestate could not be loaded\"};"


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()

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
                return render(request, 'login.html',
                              {'form': form, 'msg': 'Username or password is not correct!', 'can_not_login': True})
        else:
            return render(request, 'login.html',
                          {'form': form, 'msg': 'Username or password is not correct!', 'can_not_login': True})
    form = LoginForm()
    return render(request, 'login.html', {'form': form, 'can_not_login': False})

@login_required(login_url='/login')
def player_play_game(request, game_name):
    base_url = reverse('player_main')
    try:
        game = Game.objects.get(game_name=game_name)
        try:
            p = Purchase.objects.get(game=game, user=request.user, result=True)
            scores = Score.objects.filter(game=game)
            highscores = scores.order_by('score').reverse()[:3]
        except ObjectDoesNotExist:
            query_string = urlencode({'msg': 'The game doesn\'t belongs to you'})  # 2 category=42
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
    except ObjectDoesNotExist:
        query_string = urlencode({'msg': 'The game doesn\'t exists'})  # 2 category=42
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)



    return render(request, 'play.html', {'game': game, 'highscores': highscores})

@developer_required
def developer_modify_game(request, game_name):
    base_url = reverse('developer_main')
    try:
        game = Game.objects.get(game_name=game_name)
    except ObjectDoesNotExist:
        query_string = urlencode({'msg': 'This game doesn\'t exists'})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)
    if game.developer != request.user:

        query_string = urlencode({'msg': 'You don\'t have access to this game'})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)
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
                user.is_active = False
                user.save()
                group.user_set.add(user)
                current_site = get_current_site(request)
                mail_subject = 'Activate your blog account.'
                message = render_to_string('active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': str(user.pk),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return render(request, 'register.html', {'form': form, 'error': 'You should have received the confirmation link to your email'})
            except IntegrityError:
                return render(request, 'register.html', {'form': form, 'error': 'Username already exists'})

        else:
            return render(request, 'register.html',
                          {'form': form, 'error': 'Please check your username and password if they meet requirements.'})
    form = RegisterForm()
    return render(request, 'register.html', {'form': form, 'error': ''})

@developer_required
@login_required(login_url='/login')
def developer_main(request):
    msg = request.GET.get('msg')
    user = request.user
    # if len(user.groups.filter(name='player')) > 0:
    #     return redirect('player_main')
    game_list = Game.objects.filter(developer=user)

    # return HttpResponse('This is test developer main' + str(request.user))
    if msg is None:
        return render(request, 'developer_main.html', {'games': game_list})
    return render(request, 'developer_main.html', {'games': game_list, 'msg': msg})

@login_required(login_url='/login')
@player_required
def player_main(request):
    user = request.user
    if len(user.groups.filter(name='dev')) > 0:
        print("Not player")
        return redirect('developer_main')
    msg = request.GET.get('msg')
    purchase_history = Purchase.objects.filter(user=user, result=True)
    return render(request, 'player_main.html', {'purchase_history': purchase_history, 'msg':msg})


@login_required(login_url='/login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@developer_required
@login_required(login_url='/login')
def developer_delete_game(request, game_name):
    base_url = reverse('developer_main')
    user = request.user
    try:
        game = Game.objects.get(game_name=game_name)
    except ObjectDoesNotExist:
        query_string = urlencode({'msg': 'This game doesn\'t exists'})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)
    games = Game.objects.filter(game_name=game_name, developer=user)
    if len(games) is 0:
        base_url = reverse('developer_main')
        query_string = urlencode({'msg': 'You don\'t have permission to delete this game'})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)
    games.delete()
    base_url = reverse('developer_main')
    query_string = urlencode({'msg': 'Game deleted'})  # 2 category=42
    url = '{}?{}'.format(base_url, query_string)
    return redirect(url)

@developer_required
@login_required(login_url='/login')
def developer_create_game(request):
    user = request.user
    if request.method == 'POST':
        form = CreateGameForm(request.POST)
        if form.is_valid():
            game_name = form.cleaned_data['game_name']
            price = form.cleaned_data['game_price']
            url = form.cleaned_data['game_url']
            category = form.cleaned_data['game_category']
            if len(Game.objects.filter(game_name=game_name)) > 0:
                print('Game already exists')
                return render(request, "create_game.html", {'form': form, 'msg': 'Game already exists'})
            else:
                g = Game(game_name=game_name, price=price, developer=user, copies_sold=0, url=url)
                g.save()
                base_url = reverse('developer_main')
                query_string = urlencode({'msg': 'Game created'})  # Put message in http GET parameter
                url = '{}?{}'.format(base_url, query_string)
                return redirect(url)

        else:
            return render(request, "create_game.html", {'form': form, 'msg': 'Illegal input'})
    form = CreateGameForm()
    return render(request, "create_game.html", {'form': form})

@developer_required
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
@player_required
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
    checksum = request.GET.get('checksum')
    login(request, Purchase.objects.get(pid=pid).user)
    try:
        p = Purchase.objects.get(pid=pid, checksum=checksum)
    except ObjectDoesNotExist:
        return render(request, "buy_game_success.html",
                      {'data': request.GET.dict(), 'game_name': 'Checksum verification error!', 'success': 'failed to'})
    p.result = True
    game = p.game
    game.copies_sold += 1
    game.save()
    p.save()
    # get user object by pid and re-login
    login(request, p.user)

    return render(request, "buy_game_success.html",
                  {'data': request.GET.dict(), 'game_name': game.game_name, 'success': 'successfully'})


@login_required()
@player_required
def player_save_game(request, game_name):
    user = request.user
    if request.method == 'POST':
        print('save')
        game = Game.objects.get(game_name=game_name)
        json_score = request.POST.get('data')
        json_score = json.loads(json_score)
        return JsonResponse({'message': 'Game saved'})


@login_required()
@player_required
def player_load_game(request, game_name):
    user = request.user


@login_required()
@player_required
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

@developer_required
@login_required(login_url='/login')
def developer_sales(request):
    # list all purchase history of a game
    user = request.user
    game_history = Purchase.objects.filter(game__developer=user)

    return render(request, "game_sale.html", {'sale':game_history})


def user_confirmation(request, uuid, token):
    try:
        uid = uuid
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return render(request, "confirm_clicked.html", {'succeed': True,
                                                        'msg':'Thank you for your email confirmation. Now you can login your account.'})
    else:
        return render(request, "confirm_clicked.html", {'succeed': False,
                                                        'msg': 'Activation link is invalid! Please recheck your email'})
