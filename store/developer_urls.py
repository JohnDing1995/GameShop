from django.urls import path
from store import views
urlpatterns = [
    path('', views.developer_main,  name = 'developer_main'),
    path('create_game', views.developer_create_game),
    path('games', views.developer_sales),
    path('games/<game_name>/modify', views.developer_modify_game),
    path('games/<game_name>/delete', views.developer_delete_game)
]