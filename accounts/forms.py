from django import forms
from django.core.exceptions import ValidationError

from .models import InvitedUser, User


def _style_widget(widget_class: forms.Widget):
    return widget_class(
        attrs={
            "class": "textinput form-control",
            "placeholder": "invited_email",
        },
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=100,
        widget=_style_widget(forms.TextInput),
    )
    password = forms.CharField(
        label="Password",
        max_length=50,
        widget=_style_widget(forms.PasswordInput),
    )


class RegisterForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=100,
        widget=_style_widget(forms.TextInput),
    )
    email = forms.EmailField(
        label="Email",
        max_length=100,
        widget=_style_widget(forms.EmailInput)
    )
    password = forms.CharField(
        label="Password",
        max_length=50,
        widget=_style_widget(forms.PasswordInput),
    )
    password2 = forms.CharField(
        label="Repeat password",
        max_length=50,
        widget=_style_widget(forms.PasswordInput),
    )

    def clean(self):
        cleaned_data = super().clean()

        # Check that the registering user is invited.
        invited_user = InvitedUser.objects.filter(invited_email=cleaned_data["email"])
        if not invited_user:
            self.add_error("email", "This email is not invited to register an account.")
            # Return now so non-invited people cannot even see if username/email or
            # whatever is in use or not.
            return cleaned_data

        # Check uniqueness of username
        user = User.objects.filter(username=cleaned_data["username"])
        if user:
            self.add_error("username", "username already in use")

        # Check uniqueness of email
        user = User.objects.filter(email=cleaned_data["email"])
        if user:
            self.add_error("email", "email already in use")

        # Check that passwords must match.
        if cleaned_data["password"] != cleaned_data["password2"]:
            self.add_error("password", "Passwords don't match.")
            self.add_error("password2", "Passwords don't match.")

        return cleaned_data


class InviteForm(forms.Form):
    invited_email = forms.EmailField(
        label="Email",
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                "class": "textinput form-control",
                "placeholder": "invited_email",
            },
        ),
    )
    repeat_email = forms.EmailField(
        label="Repeat Email",
        max_length=100,
        widget=_style_widget(forms.EmailInput),
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["invited_email"] != cleaned_data["repeat_email"]:
            msg = "Emails must match."
            self.add_error("invited_email", msg)
            self.add_error("repeat_email", msg)
            return cleaned_data

        # Check if this email is already invited.
        invited_user = InvitedUser.objects.filter(
            invited_email=cleaned_data["invited_email"]
        )
        if invited_user:
            raise ValidationError(
                "Email %(invited_email)s is already invited",
                params={"invited_email": cleaned_data["invited_email"]},
                code="already_invited",
            )

        return cleaned_data
