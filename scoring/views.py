from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from .forms import ProfileForm
from .models import Game, Player

def index(request: HttpRequest):
    if request.user.is_authenticated:
        if not request.user.player_set.first():
            return HttpResponseRedirect(reverse("scoring:profile"))

    template = loader.get_template("scoring/index.html")
    context = {
        "games": Game.objects.all()
    }
    return HttpResponse(template.render(context, request))


# TODO: Do not allow anonymous users to access this view.
def profile(request: HttpRequest):
    # If the user doesn't have yet a player, we need to create one now.
    player = request.user.player_set.first()
    if not player:
        player = Player(
            displayname=request.user.username,
            user=request.user
        )

    if request.method == "POST":
        form = ProfileForm(request.POST)
        try:
            a = form.is_valid()
        except Exception as exc:
            print(exc)
        if form.is_valid():
            displayname = form.cleaned_data["displayname"]
            player.displayname = displayname
            player.save()
            return HttpResponseRedirect(reverse("scoring:index"))
    else:  # GET
        form = ProfileForm(instance=player)
        template = loader.get_template("scoring/profile.html")

    # This return is not in the else because it will render errors for the POST case.
    context = {
        "form": form,
    }
    return render(request, "scoring/profile.html", context)


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
    messages.debug(request, "Score saved.")
    return HttpResponseRedirect(reverse("scoring:index"))
