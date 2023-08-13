from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.urls import reverse

from .models import Board, Game, Player, Scorer, ScoringCategory, Score


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Player
        exclude = ["user", "role"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "textinput form-control"
            field.widget.attrs["placeholder"] = field_name


class AddGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "textinput form-control"
            field.widget.attrs["placeholder"] = field_name

    def clean(self):
        cleaned_data = super().clean()

        # Check if the same game already exists in the DB.
        clean_name = Game.get_clean_name(cleaned_data["name"])
        game = Game.objects.filter(name=clean_name).first()
        if game:
            self.add_error("name", f"Game already exists as {clean_name}.")

        return cleaned_data


ScoringCategoryFormSet = forms.inlineformset_factory(Game, ScoringCategory, fields=["name"])


def get_scoring_category_formset(game: Game, post_data = None):
    if post_data is None:
        formset = ScoringCategoryFormSet(instance=game)
    else:
        formset = ScoringCategoryFormSet(post_data, instance=game)
    # Add styling
    for form in formset:
        for field_name, field in form.fields.items():
            if field_name == "DELETE":
                field.widget = forms.HiddenInput()
            else:
                field.widget.attrs["class"] = "textinput form-control"
                field.widget.attrs["placeholder"] = field_name
    return formset


def scoring_category_formset_is_valid(formset, *args, **kwargs):
    # Only keep forms with data: this can be undesired when emptying existing values
    # (meaning leaving blank a value that previously had data) must be forbidden, but
    # I want to allow it to delete an existing scoring category by just leaving it as
    # an empty field.
    formset.forms = [form for form in formset if form["name"].value()]
    return super(ScoringCategoryFormSet, formset).is_valid(*args, **kwargs)


ScoringCategoryFormSet.is_valid = scoring_category_formset_is_valid


AddScorersFormSet = forms.inlineformset_factory(Board, Scorer, fields=["name"])


def add_scorers_formset_is_valid(formset, *args, **kwargs):
    forms_with_name = []
    for form in formset:
        if not form["name"].value():
            if form.instance.pk is not None:
                form.instance.delete()
            continue
        forms_with_name.append(form)
    formset.forms = forms_with_name
    return super(AddScorersFormSet, formset).is_valid(*args, **kwargs)


AddScorersFormSet.is_valid = add_scorers_formset_is_valid


class AddScorersFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        game_name_or_board_pk = kwargs.pop("game_name_or_board_pk")
        super().__init__(*args, **kwargs)

        self.form_method = "post"
        self.form_action = reverse(
            "scoring:add_board_players", args=(game_name_or_board_pk,)
        )

        self.field_class = "form-floating"

        self.layout = Layout(
            FloatingField("name"),
        )

        self.add_input(
            Submit(
                "save_and_add_more",
                "Save and add more",
                css_class="w-100 btn btn-lg btn-primary",
            )
        )
        self.add_input(
            Submit(
                "save_and_exit",
                "Save and exit",
                css_class="w-100 btn btn-lg btn-primary",
            )
        )


class AddYourScorerForm(forms.ModelForm):
    class Meta:
        model = Scorer
        fields = ("name",)
        labels = {
            "name": "Your name",
        }


class AddYourScoreValueForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ("value",)


def add_your_scores_form_factory(form_name: str, sc_names: list[str]):
    form_fields = {
            "name": forms.CharField(max_length=50, label="Your name"),
        }
    score_fields = {
        scoring_category: forms.IntegerField(label=scoring_category)
        for scoring_category in sc_names
    }
    form_fields.update(score_fields)
    Form = type(
        form_name,
        (forms.Form,),
        form_fields.copy(),  # If I dont provide a copy then the dict is mutated within.
    )

    def form_init(self, *args, **kwargs):
        board_pk = kwargs.pop("board_pk", None)
        super(Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_method = "post"
        if board_pk is not None:
            self.helper.form_action = reverse("scoring:add_your_score", args=(board_pk,))

        self.helper.field_class = "form-floating"

        floating_fields = [FloatingField(field_name) for field_name in form_fields]
        self.helper.layout = Layout(*floating_fields)

        self.helper.add_input(
            Submit("save", "Save", css_class="w-100 btn btn-lg btn-primary")
        )

    Form.__init__ = form_init

    return Form
