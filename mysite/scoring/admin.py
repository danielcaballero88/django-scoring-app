from django.contrib import admin

from .models import Game, ScoringCategory



class ScoringCategoryInLine(admin.TabularInline):
    model = ScoringCategory
    extra = 1



class GameAdmin(admin.ModelAdmin):
    inlines= [ScoringCategoryInLine]


admin.site.register(Game, GameAdmin)
