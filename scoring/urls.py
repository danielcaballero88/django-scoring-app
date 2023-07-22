from django.urls import path

from . import views

app_name = "scoring"
urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.profile, name="profile"),
    path("edit_games/", views.edit_games, name="edit_games"),
    path("add_game/", views.add_game, name="add_game"),
    path(
        "add_scoring_categories/<str:game_name>/",
        views.add_scoring_categories,
        name="add_scoring_categories",
    ),
    path("score/<str:game_name>/", views.score, name="score"),
    path("save/<str:game_name>/", views.save, name="save"),
]
