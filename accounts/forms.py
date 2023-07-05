from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_bootstrap5.bootstrap5 import FloatingField
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    email = forms.EmailField(label="Email", max_length=100)
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", max_length=50, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_method = "post"
        self.helper.form_action = "accounts:register"

        self.helper.field_class = "form-floating"

        self.helper.layout = Layout(
            FloatingField("username", "email", "password", "password2"),
        )

        self.helper.add_input(Submit("register", "Register", css_class='w-100 btn btn-lg btn-primary'))

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["password"] != cleaned_data["password2"]:
            self.add_error("password", "Passwords don't match.")
            self.add_error("password2", "Passwords don't match.")

class InviteForm(forms.Form):
    invited_email = forms.EmailField(label="Email", max_length=100)
    repeat_email = forms.EmailField(label="Repeat Email", max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_method = "post"
        self.helper.form_action = "accounts:invite"

        self.helper.field_class = "form-floating"

        self.helper.layout = Layout(
            FloatingField("invited_email", "repeat_email"),
        )

        self.helper.add_input(Submit("invite", "Invite", css_class='w-100 btn btn-lg btn-primary'))
