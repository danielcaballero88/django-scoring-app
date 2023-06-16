from django.http import HttpRequest, HttpResponse
from django.template import loader

def index(request: HttpRequest):
    template = loader.get_template("scoring/index.html")
    context = {
        "game": request.GET.get("game"),
    }
    return HttpResponse(template.render(context, request))
