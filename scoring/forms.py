from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_bootstrap5.bootstrap5 import FloatingField
from django.forms import ModelForm, inlineformset_factory, modelform_factory
from django.urls import reverse

from .models import Player, Game, ScoringCategory, Board, Scorer


class ProfileForm(ModelForm):

    class Meta:
        model = Player
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_method = "post"
        self.helper.form_action = "scoring:profile"

        self.helper.field_class = "form-floating"

        self.helper.layout = Layout(
            FloatingField("displayname"),
        )

        self.helper.add_input(Submit("save", "Save", css_class='w-100 btn btn-lg btn-primary'))


class AddGameForm(ModelForm):
    class Meta:
        model = Game
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_method = "post"
        self.helper.form_action = "scoring:add_game"

        self.helper.field_class = "form-floating"

        self.helper.layout = Layout(
            FloatingField("name"),
        )

        self.helper.add_input(Submit("save", "Save", css_class='w-100 btn btn-lg btn-primary'))

    def clean(self):
        cleaned_data = super().clean()

        # Check if the same game already exists in the DB.
        clean_name = Game.get_clean_name(cleaned_data["name"])
        game = Game.objects.filter(name=clean_name).first()
        if game:
            self.add_error("name", f"Game already exists as {clean_name}.")

        return cleaned_data


ScoringCategoryFormSet = inlineformset_factory(Game, ScoringCategory, fields=["name"])

class ScoringCategoryFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        game_name = kwargs.pop("game_name")
        super().__init__(*args, **kwargs)

        self.form_method = "post"
        self.form_action = reverse("scoring:edit_game", args=(game_name,))

        self.field_class = "form-floating"

        self.layout = Layout(
            FloatingField("name"),
        )

        self.add_input(Submit("save_and_add_more", "Save and add more", css_class='w-100 btn btn-lg btn-primary'))
        self.add_input(Submit("save_and_exit", "Save and exit", css_class='w-100 btn btn-lg btn-primary'))

def scoring_category_formset_is_valid(formset, *args, **kwargs):
    # Only keep forms with data: this can be undesired when emptying existing values
    # (meaning leaving blank a value that previously had data) must be forbidden, but
    # I want to allow it to delete an existing scoring category by just leaving it as
    # an empty field.
    formset.forms = [form for form in formset if form["name"].value()]
    return super(ScoringCategoryFormSet, formset).is_valid(*args, **kwargs)

ScoringCategoryFormSet.is_valid = scoring_category_formset_is_valid


AddScorersFormSet = inlineformset_factory(Board, Scorer, fields=["name"])

class AddScorersFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        board_pk = kwargs.pop("board_pk")
        super().__init__(*args, **kwargs)

        self.form_method = "post"
        self.form_action = reverse("scoring:add_board_players", args=(str(board_pk),))

        self.field_class = "form-floating"

        self.layout = Layout(
            FloatingField("name"),
        )

        self.add_input(Submit("save_and_add_more", "Save and add more", css_class='w-100 btn btn-lg btn-primary'))
        self.add_input(Submit("save_and_exit", "Save and exit", css_class='w-100 btn btn-lg btn-primary'))
