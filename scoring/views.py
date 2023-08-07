from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views.decorators.http import require_POST


from .forms import ProfileForm, AddGameForm, ScoringCategoryFormSet, ScoringCategoryFormSetHelper, AddScorersFormSet, AddScorersFormSetHelper
from .models import Game, Player, ScoringCategory, Board, Scorer


def index(request: HttpRequest):
    if request.user.is_authenticated:
        if not hasattr(request.user, "player"):
            return HttpResponseRedirect(reverse("scoring:profile"))

    template = loader.get_template("scoring/index.html")
    context = {
        "games": Game.objects.all()
    }
    return HttpResponse(template.render(context, request))


@login_required
def profile(request: HttpRequest):
    # If the user doesn't have yet a player, we need to create one now.
    player = getattr(request.user, "player", None)
    if not player:
        player = Player(
            displayname=request.user.username,
            user=request.user
        )
        player.save()

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


@login_required
def edit_games(request: HttpRequest):
    template = loader.get_template("scoring/edit_games.html")
    context = {
        "games": Game.objects.all()
    }
    return HttpResponse(template.render(context, request))


@login_required
def add_game(request: HttpRequest):
    if request.method == "POST":
        form = AddGameForm(request.POST)
        if form.is_valid():
            game = Game(name=form.cleaned_data["name"])
            game.save()
            return HttpResponseRedirect(reverse("scoring:edit_game", args=(game.name,)))

    else:
        form = AddGameForm()

    context = {
        "form": form,
    }
    return render(request, "scoring/add_game.html", context)


@login_required
def edit_game(request: HttpRequest, game_name: str):
    clean_game_name = Game.get_clean_name(game_name)
    game = Game.objects.filter(name=clean_game_name).first()
    if not game:
        messages.error(request, f"Game {game_name} not found.")
        return HttpResponseRedirect(reverse("scoring:index"))

    if request.method == "POST":
        formset = ScoringCategoryFormSet(request.POST, instance=game)
        if formset.is_valid():
            game.scoringcategory_set.all().delete()
            for form in formset:
                if "name" not in form.cleaned_data:
                    continue
                sc_name = form.cleaned_data["name"]
                sc = ScoringCategory(
                    game=game,
                    name=sc_name,
                )
                sc.save()

            if request.POST.get("save_and_add_more"):
                return HttpResponseRedirect(reverse("scoring:edit_game", args=(game_name,)))
            else: # save_and_exit
                return HttpResponseRedirect(reverse("scoring:edit_games"))

    else:
        formset = ScoringCategoryFormSet(instance=game)

    context = {
        "game_name": game_name,
        "formset": formset,
        "helper": ScoringCategoryFormSetHelper(game_name=game_name),
    }

    return render(
        request,
        "scoring/edit_game.html",
        context,
    )

@login_required
@require_POST
def delete_game(request: HttpRequest, game_name: str):
    clean_game_name = Game.get_clean_name(game_name)
    Game.objects.filter(name=clean_game_name).delete()
    return HttpResponseRedirect(reverse("scoring:edit_games"))


@login_required
def add_board(request: HttpRequest):
    template = loader.get_template(f"scoring/add_board.html")
    context = {
        "games": Game.objects.all()
    }
    return HttpResponse(template.render(context, request))


@login_required
def add_board_players(request: HttpRequest, game_name_or_board_pk: str):
    try:
        board_pk = int(game_name_or_board_pk)
        board = get_object_or_404(Board, pk=board_pk)
        game = board.game
        game_name = game.name
    except ValueError as exc:
        game_name = game_name_or_board_pk
        clean_game_name = Game.get_clean_name(game_name)
        game = Game.objects.filter(name=clean_game_name).first()
        board = Board(game=game, player=request.user.player)
        board.save()
        board_pk = board.pk

    if not game:
        messages.error(request, f"Game {game_name} not found.")
        return HttpResponseRedirect(reverse("scoring:index"))

    if request.method == "POST":
        formset = AddScorersFormSet(request.POST, instance=board)
        if formset.is_valid():
            # Create a new board:
            for form in formset:
                if "name" not in form.cleaned_data:
                    continue
                scorer_name = form.cleaned_data["name"]
                scorer = Scorer(
                    name=scorer_name,
                    board=board,
                )
                scorer.save()

            if request.POST.get("save_and_add_more"):
                return HttpResponseRedirect(reverse("scoring:add_board_players", args=(str(board_pk),)))
            else: # save_and_exit
                messages.info(request, f"Success creating board {board_pk} with players {board.scorer_set.all()}")
                return HttpResponseRedirect(reverse("scoring:index"))

    else:
        formset = AddScorersFormSet(instance=board)

    context = {
        "board_pk": board_pk,
        "game_name": game_name,
        "formset": formset,
        "helper": AddScorersFormSetHelper(board_pk=board_pk),
    }

    return render(
        request,
        "scoring/edit_game.html",
        context,
    )

@login_required
def boards_list(request: HttpRequest):
    player = request.user.player
    boards = player.board_set.all()
    context = {
        "boards": boards,
    }
    template = loader.get_template("scoring/boards_list.html")
    return HttpResponse(template.render(context, request))

@login_required
def board_score(request: HttpRequest, board_pk: int):
    board = get_object_or_404(Board, pk=board_pk)
    game = board.game
    scoring_categories = game.scoringcategory_set.all()
    scorers = board.scorer_set.all()
    template = loader.get_template(f"scoring/board_score.html")
    context = {
        "board": board,
        "game": game,
        "scoring_categories": scoring_categories,
        "scorers": scorers,
    }
    return HttpResponse(template.render(context, request))

@login_required
@require_POST
def delete_board(request: HttpRequest, board_pk: int):
    board = get_object_or_404(Board, pk=board_pk)
    board.delete()
    messages.info(request, f"Board {board_pk} deleted.")
    return HttpResponseRedirect(reverse("scoring:boards_list"))

def save(request: HttpRequest, game_name: str):
    messages.debug(request, "Score saved.")
    return HttpResponseRedirect(reverse("scoring:index"))
