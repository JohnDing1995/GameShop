from django.urls import path
from store import views
urlpatterns = [
    path('', views.player_main, name= 'player_main'),
    path('games', views.player_list_games),
    path('games/<game_name>', views.player_play_game)
]