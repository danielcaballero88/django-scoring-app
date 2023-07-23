from django.contrib import admin

from .models import Game, Player, ScoringCategory, Board, Scorer



class ScoringCategoryInLine(admin.TabularInline):
    model = ScoringCategory
    extra = 1



class GameAdmin(admin.ModelAdmin):
    inlines= [ScoringCategoryInLine]


class BoardInLine(admin.TabularInline):
    model = Board
    extra = 1


class ScorerInLine(admin.TabularInline):
    model = Scorer
    extra = 3


class BoardAdmin(admin.ModelAdmin):
    inlines = [ScorerInLine]


class PlayerAdmin(admin.ModelAdmin):
    inlines = [BoardInLine]


admin.site.register(Game, GameAdmin)

admin.site.register(Player, PlayerAdmin)

admin.site.register(Board, BoardAdmin)
