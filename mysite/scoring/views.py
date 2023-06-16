from django.http import HttpRequest, HttpResponse

def index(request: HttpRequest):
    return HttpResponse(f"Hello, world. You're at the scoring app index for game: {request.GET.get('game')}")
