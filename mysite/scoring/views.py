from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from .models import Game

def index(request: HttpRequest):
    template = loader.get_template("scoring/index.html")
    context = {
        "games": Game.objects.all()
    }
    return HttpResponse(template.render(context, request))


def score(request: HttpRequest, game_name: str):
    template = loader.get_template(f"scoring/score.html")
    game = Game.objects.get(name=game_name)
    scoring_categories = game.scoringcategory_set.all()
    context = {
        "game": game,
        "scoring_categories": scoring_categories,
    }
    return HttpResponse(template.render(context, request))


def save(request: HttpRequest, game_name: str):
    return HttpResponseRedirect(reverse("scoring:index"))
