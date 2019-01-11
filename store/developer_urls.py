from django.urls import path
from store import views
urlpatterns = [
    path('', views.developer_main,  name = 'player_main'),
    path('games', views.developer_list_games),
    path('games/<int:game_id>', views.developer_set_game)
]