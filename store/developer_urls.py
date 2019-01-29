
from django.urls import path
from store import views
urlpatterns = [
    path('', views.developer_main,  name = 'developer_main'),
    path('create_game', views.developer_create_game),
    path('games/<game_name>', views.developer_game_buyer),
    path('games/<game_name>/modify', views.developer_modify_game)
]