from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_bootstrap5.bootstrap5 import FloatingField
from django.forms import ModelForm

from .models import Player, Game


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
