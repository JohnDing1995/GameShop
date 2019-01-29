from django.urls import path
from store import views
urlpatterns = [
    path('', views.player_main, name= 'player_main'),
    path('store', views.store, name='store'),
    path('games/<game_name>', views.player_play_game),
    path('games/<game_name>/buy', views.player_buy_game),
    path('games/<game_name>/save', views.player_save_game),
    path('games/<game_name>/load', views.player_load_game),
    path('games/<game_name>/submit_score', views.player_submit_score),

]