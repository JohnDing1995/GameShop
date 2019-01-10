from django.urls import path
from store import views
urlpatterns = [
    path('games', views.player_list_games),
    path('games/<int:game_id>', views.player_play_game)
]