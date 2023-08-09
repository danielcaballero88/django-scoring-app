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
    path(
        "add_board_players/<str:game_name_or_board_pk>/",
        views.add_board_players,
        name="add_board_players",
    ),
    path("boards_list/", views.boards_list, name="boards_list"),
    path("delete_board/<int:board_pk>/", views.delete_board, name="delete_board"),
    path("board_score/<int:board_pk>/", views.board_score, name="board_score"),
    path("add_your_score/<int:board_pk>/", views.add_your_score, name="add_your_score"),
]
