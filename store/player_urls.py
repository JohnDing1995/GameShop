from django.urls import path
from store import views
urlpatterns = [
    path('', views.player_main, name= 'player_main'),
    path('games', views.player_list_games),
    path('games/<int:game_id>', views.player_play_game)
]