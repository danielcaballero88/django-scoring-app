from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

def index(request: HttpRequest):
    template = loader.get_template("scoring/index.html")
    context = {}
    return HttpResponse(template.render(context, request))


def game(request: HttpRequest, game: str):
    template = loader.get_template(f"scoring/{game}.html")
    context = {
        "game": game,
    }
    return HttpResponse(template.render(context, request))


def save(request: HttpRequest, game: str):
    return HttpResponseRedirect(reverse("scoring:game", args=(game,)))
