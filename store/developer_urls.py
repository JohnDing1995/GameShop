from django.urls import path
from store import views
urlpatterns = [
    path('', views.developer_main,  name = 'developer_main'),
    path('create_game', views.developer_create_game),
    path('games', views.developer_list_games),
    path('games/<int:game_id>', views.developer_game_buyer),
    path('games/<int:game_id>/modify', views.developer_set_game)
]