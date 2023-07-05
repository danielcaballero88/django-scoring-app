from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import LoginForm, RegisterForm, InviteForm
from .models import InvitedUser


def login(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                # A backend authenticated the credentials
                django_login(request, user)
                messages.success(request, f"Login success for {username}")
            else:
                # No backend authenticated the credentials
                messages.error(request, f"Login error for {username}")
            # redirect to a new URL:
            return HttpResponseRedirect(reverse("scoring:index"))
        # else: the render statement at the end of this view will render
        # the form again showing the errors that should be attached to
        # the form in the POST request (?... need to check of course)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def logout(request):
    user: User = request.user
    if user.is_authenticated:
        django_logout(request)
        messages.info(request, "User logged out.")
        return HttpResponseRedirect(reverse("scoring:index"))
    else:
        messages.error(request, "No user logged in.")
        return HttpResponseRedirect(reverse("scoring:index"))


def register(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            try:
                # I'll validate that the username must be unique here, but it's better
                # to do that in the form in the future.
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                )
                user.save()
            except IntegrityError as exc:
                if (
                    hasattr(exc, "args")
                    and isinstance(exc.args, tuple)
                    and isinstance(exc.args[0], str)
                    and "UNIQUE" in exc.args[0]
                ):
                    form.add_error("username", "username is already in use")
                else:
                    raise exc
            else:
                messages.success(request, f"User {username} was registered correctly.")
                # redirect to a new URL:
                return HttpResponseRedirect(reverse("scoring:index"))
        # else: the render statement at the end of this view will render
        # the form again showing the errors that should be attached to
        # the form in the POST request (?... need to check of course)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def invite(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            invited_email = form.cleaned_data["invited_email"]
            repeat_email = form.cleaned_data["repeat_email"]
            try:
                # inviter = User.objects.get()
                # invited_user = InvitedUser(
                #     inviter =
                # )
                # user = User.objects.create_user(
                #     username=username,
                #     email=email,
                #     password=password,
                # )
                # user.save()
                ...
            except IntegrityError as exc:
                if (
                    hasattr(exc, "args")
                    and isinstance(exc.args, tuple)
                    and isinstance(exc.args[0], str)
                    and "UNIQUE" in exc.args[0]
                ):
                    messages.error(
                        request, f"Cannot register user {username}, alrady exists."
                    )
                else:
                    raise exc
            else:
                messages.success(request, f"User {username} was registered correctly.")
                # redirect to a new URL:
                return HttpResponseRedirect(reverse("scoring:index"))
        # else: the render statement at the end of this view will render
        # the form again showing the errors that should be attached to
        # the form in the POST request (?... need to check of course)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})
