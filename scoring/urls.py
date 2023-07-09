from django.urls import path

from . import views

app_name = "scoring"
urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.profile, name="profile"),
    path("score/<str:game_name>/", views.score, name="score"),
    path("save/<str:game_name>/", views.save, name="save"),
]
