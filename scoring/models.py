from django.db import models
from accounts.models import User


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    displayname = models.CharField(max_length=100)

    def __str__(self):
        return f"Player: {self.displayname}"


class Game(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Game: {self.name}"


class ScoringCategory(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"Scoring Category: {self.name} for {self.game.name}"


class Board(models.Model):
    game = models.ForeignKey(Game, on_delete=models.RESTRICT)
    player = models.ManyToManyField(Player)

    def __str__(self):
        return f"Board: {self.pk}, playing {self.game} - {self.player}"


class Score(models.Model):
    player = models.ForeignKey(Player, on_delete=models.RESTRICT)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    scoring_category = models.ForeignKey(ScoringCategory, on_delete=models.RESTRICT)
    value = models.IntegerField(default=0)

    def __str__(self):
        return f"Score for {self.player.name} for {self.scoring_category.name}: {self.value}"
