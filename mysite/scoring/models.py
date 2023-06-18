from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=100)


class Game(models.Model):
    name = models.CharField(max_length=100)


class ScoringCategory(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)


class Board(models.Model):
    game = models.ForeignKey(Game, on_delete=models.RESTRICT)


class BoardPlayer(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.RESTRICT)


class Score(models.Model):
    player = models.ForeignKey(Player, on_delete=models.RESTRICT)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    scoring_category = models.ForeignKey(ScoringCategory, on_delete=models.RESTRICT)
    value = models.IntegerField(default=0)
