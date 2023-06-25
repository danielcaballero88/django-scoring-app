from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import LoginForm, RegisterForm


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
