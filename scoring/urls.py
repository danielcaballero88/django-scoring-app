from django.urls import path

from . import views

app_name = "scoring"
urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.profile, name="profile"),
    path("edit_games/", views.edit_games, name="edit_games"),
    path("add_game/", views.add_game, name="add_game"),
    path("edit_game/<str:game_name>/", views.edit_game, name="edit_game"),
    path("delete_game/<str:game_name>/", views.delete_game, name="delete_game"),
    path("add_board", views.add_board, name="add_board"),
    path("score/<str:game_name>/", views.score, name="score"),
    path("save/<str:game_name>/", views.save, name="save"),
]
