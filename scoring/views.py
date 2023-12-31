from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import (
    AddGameForm,
    get_add_scorers_formset,
    ProfileForm,
    get_scoring_category_formset,
    add_your_scores_form_factory,
)
from .models import Board, Game, Player, Score, Scorer, ScoringCategory


def index(request: HttpRequest):
    if request.user.is_authenticated:
        if not hasattr(request.user, "player"):
            return HttpResponseRedirect(reverse("scoring:profile"))

    template = loader.get_template("scoring/index.html")
    context = {"games": Game.objects.all()}
    return HttpResponse(template.render(context, request))


@login_required
def profile(request: HttpRequest):
    # If the user doesn't have yet a player, we need to create one now.
    player = getattr(request.user, "player", None)
    if not player:
        player = Player(displayname=request.user.username, user=request.user)
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
            messages.success(
                request,
                f"Successfully updated profile for username: {request.user.username}."
                f" New displayname: {player.displayname}."
            )
            return HttpResponseRedirect(reverse("scoring:index"))
    else:  # GET
        form = ProfileForm(instance=player)

    # This return is not in the else because it will render errors for the POST case.
    context = {
        "form": form,
    }
    return render(request, "scoring/profile.html", context)


@login_required
def edit_games(request: HttpRequest):
    template = loader.get_template("scoring/edit_games.html")
    context = {"games": Game.objects.all()}
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
        # formset = ScoringCategoryFormSet(request.POST, instance=game)
        formset = get_scoring_category_formset(
            game=game,
            post_data=request.POST,
        )
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
                return HttpResponseRedirect(
                    reverse("scoring:edit_game", args=(game_name,))
                )
            else:  # save_and_exit
                return HttpResponseRedirect(reverse("scoring:index"))

    else: # GET
        formset = get_scoring_category_formset(game=game)

    context = {
        "game_name": game_name,
        "formset": formset,
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
    context = {"games": Game.objects.all()}
    return HttpResponse(template.render(context, request))


@login_required
def add_board_players(request: HttpRequest, game_name_or_board_pk: str):
    try:
        # Case where board_pk is passed: editing an existing board.
        board_pk = int(game_name_or_board_pk)
        board = get_object_or_404(Board, pk=board_pk)
        game = board.game
    except ValueError as exc:
        # Case where game_name is passed: creating a new board.
        game_name = game_name_or_board_pk
        clean_game_name = Game.get_clean_name(game_name)
        game = Game.objects.filter(name=clean_game_name).first()
        board = Board(game=game, player=request.user.player)

    if not game:
        messages.error(request, f"Game {game_name} not found.")
        return HttpResponseRedirect(reverse("scoring:index"))

    if request.method == "POST":
        if board.pk is None:
            # A new board is being created
            board.save()
        game = board.game
        formset = get_add_scorers_formset(board=board, post_data=request.POST)
        if formset.is_valid():
            # Create a new board:
            for form in formset:
                if "name" not in form.cleaned_data:
                    continue
                scorer: Scorer = form.instance
                scorer.save()

            if request.POST.get("save_and_add_more"):
                return HttpResponseRedirect(
                    reverse("scoring:add_board_players", args=(str(board.pk),))
                )
            else:  # save_and_exit
                return HttpResponseRedirect(
                    reverse("scoring:board_score", args=(str(board.pk),))
                )

    else:  # GET
        formset = get_add_scorers_formset(board=board)

    context = {
        "game_name": game.name,
        "game_name_or_board_pk": game_name_or_board_pk,  # needed for the form action
        "formset": formset,
    }

    return render(
        request,
        "scoring/add_board_players.html",
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

    if request.method == "POST":
        score_keys = (key for key in request.POST if key.startswith("score"))
        for score_key in score_keys:
            score_key_parts = score_key.split("-")
            scoring_category_pk = int(score_key_parts[1])
            scorer_pk = int(score_key_parts[2])
            score = Score.objects.filter(
                board_id=board_pk,
                scorer_id=scorer_pk,
                scoring_category_id=scoring_category_pk,
            ).first()
            if score is None:
                score = Score(
                    board_id=board_pk,
                    scorer_id=scorer_pk,
                    scoring_category_id=scoring_category_pk,
                    value=0,
                )
            value_str = request.POST[score_key]
            if value_str:
                value = int(value_str)
            else:
                value = 0
            score.value = value
            score.save()
        return HttpResponseRedirect(reverse("scoring:board_score", args=(board_pk,)))

    game = board.game
    scoring_categories = game.scoringcategory_set.all()
    scorers = board.scorer_set.all()
    template = loader.get_template(f"scoring/board_score.html")
    score_values = {}
    totals = {}
    for scorer in scorers:
        score_values[scorer.pk] = {}
        totals[scorer.pk] = 0
        for scoring_category in scoring_categories:
            score_key = f"score-{scoring_category.pk}-{scorer.pk}"
            score = Score.objects.filter(
                board_id=board_pk,
                scoring_category_id=scoring_category.pk,
                scorer_id=scorer.pk,
            ).first()
            if score:
                score_value = score.value
            else:
                score_value = 0
            score_values[scorer.pk][scoring_category.pk] = score_value
            totals[scorer.pk] += score_value
    context = {
        "board": board,
        "game": game,
        "scoring_categories": scoring_categories,
        "scorers": scorers,
        "has_scorers": len(scorers) > 0,
        "score_values": score_values,
        "totals": totals,
        "url_share": request.build_absolute_uri(reverse("scoring:add_your_score", args=(board.pk,))),
    }
    return HttpResponse(template.render(context, request))


@login_required
@require_POST
def delete_board(request: HttpRequest, board_pk: int):
    board = get_object_or_404(Board, pk=board_pk)
    board.delete()
    messages.info(request, f"Board {board_pk} deleted.")
    return HttpResponseRedirect(reverse("scoring:boards_list"))


def add_your_score(request: HttpRequest, board_pk: int):
    # TODO: create links with a jwt token with expiration so it's easy to reject
    # requests after 5 min. Also make sure to only allow a maximum number of scorers
    # per board to avoid attacks.
    board = get_object_or_404(Board, pk=board_pk)
    scoring_categories = board.game.scoringcategory_set.all()
    sc_names = [sc.name for sc in scoring_categories]
    AddYourScoresForm = add_your_scores_form_factory("AddYourScoresForm", sc_names)

    if request.method == "POST":
        form = AddYourScoresForm(request.POST)
        if form.is_valid():
            scorer_name = form.cleaned_data["name"]
            scorer = Scorer(
                name=scorer_name,
                board=board,
            )
            scorer.save()
            for sc in scoring_categories:
                score_value = form.cleaned_data[sc.name]
                score = Score(
                    value=score_value,
                    board=board,
                    scorer=scorer,
                    scoring_category=sc,
                )
                score.save()
            messages.success(request, "Thanks for providing your score!")
            return HttpResponseRedirect(reverse("scoring:index"))

    form = AddYourScoresForm()
    template = loader.get_template("scoring/add_your_score.html")
    context = {
        "board_pk": board_pk,
        "form": form,
    }

    return HttpResponse(template.render(context, request))
