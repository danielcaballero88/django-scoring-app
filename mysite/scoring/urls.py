from django.urls import path

from . import views

app_name = "scoring"
urlpatterns = [
    path("", views.index, name="index"),
    path("score/<str:game>/", views.game, name="game"),
    path("save/", views.save, name="save")
]
