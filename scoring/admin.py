from django.contrib import admin

from .models import Game, Player, ScoringCategory



class ScoringCategoryInLine(admin.TabularInline):
    model = ScoringCategory
    extra = 1



class GameAdmin(admin.ModelAdmin):
    inlines= [ScoringCategoryInLine]


class PlayerAdmin(admin.ModelAdmin):
    ...


admin.site.register(Game, GameAdmin)

admin.site.register(Player, PlayerAdmin)
