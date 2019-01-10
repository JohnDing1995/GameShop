from django.urls import path
from store import views
urlpatterns = [
    path('games', views.developer_list_games),
    path('games/<int:game_id>', views.developer_set_game)
]