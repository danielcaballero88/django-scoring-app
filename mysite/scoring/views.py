from django.http import HttpRequest, HttpResponse
from django.template import loader

def index(request: HttpRequest):
    template = loader.get_template("scoring/index.html")
    context = {}
    return HttpResponse(template.render(context, request))


def game(request: HttpRequest, game: str):
    template = loader.get_template(f"scoring/{game}.html")
    context = {}
    return HttpResponse(template.render(context, request))


def save(request: HttpRequest):
    return HttpResponse(f"{request.POST.get('score-21')}")
