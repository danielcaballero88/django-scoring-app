from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_bootstrap5.bootstrap5 import FloatingField
from django import forms
from django.urls import reverse


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    email = forms.EmailField(label="Email", max_length=100)
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_method = "post"
        self.helper.form_action = "accounts:register"

        self.helper.field_class = "form-floating"

        self.helper.layout = Layout(
            FloatingField("username", "email", "password"),
        )

        self.helper.add_input(Submit("register", "Register", css_class='w-100 btn btn-lg btn-primary'))
