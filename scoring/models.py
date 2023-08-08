from django.db import models
from accounts.models import User

import re

class Player(models.Model):
    class Role(models.TextChoices):
        REGULAR = "regular"
        EDITOR = "editor"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    displayname = models.CharField(max_length=100)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.REGULAR,
    )

    @property
    def is_editor(self):
        return self.role == self.Role.EDITOR

    def __str__(self):
        return f"Player: {self.displayname}"


class Game(models.Model):
    name = models.CharField(max_length=100)

    @staticmethod
    def get_clean_name(name):
        # Regex for a number of consequtive non-letter non-digit chars.
        rgx = r"(\W|_)+"
        # Clean leading and trailing non letters or numbers.
        clean_name = re.sub(rf"^{rgx}|{rgx}$", "", name)
        # Clean spaces, hyphens, etc, in the middle, and replace with a
        # single space to avoid difference in using, e.g.,  - vs _.
        clean_name = re.sub(rgx, " ", clean_name)
        # capitalize
        clean_name = clean_name.capitalize()

        return clean_name

    def save(self, *args, **kwargs):
        self.name = self.get_clean_name(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Game: {self.name}"


class ScoringCategory(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"Scoring Category: {self.name} for {self.game.name}"


class Board(models.Model):
    game = models.ForeignKey(Game, on_delete=models.RESTRICT)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return f"Board: {self.pk}, playing {self.game} - {self.player}"


class Scorer(models.Model):
    name = models.CharField(max_length=50)
    display_name = models.CharField(max_length=5)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.display_name = self.name[:3]
        super().save(*args, *kwargs)

    def __str__(self):
        return f"Scorer: {self.name}"


class Score(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    scorer = models.ForeignKey(Scorer, on_delete=models.CASCADE)
    scoring_category = models.ForeignKey(ScoringCategory, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return f"Score for {self.scorer.name} for {self.scoring_category.name}: {self.value}"
