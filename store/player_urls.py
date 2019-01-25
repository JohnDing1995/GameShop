from django.urls import path
from store import views
urlpatterns = [
    path('', views.player_main, name= 'player_main'),
    path('store', views.store, name='store'),
    path('games/<game_name>', views.player_play_game),
    path('games/<game_name>/buy', views.player_buy_game)

]