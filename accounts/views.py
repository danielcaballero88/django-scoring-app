from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import LoginForm, RegisterForm, InviteForm
from .models import User, InvitedUser


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

            # I'll validate that the username must be unique here, but it's better
            # to do that in the form in the future.
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            user.save()

            messages.success(request, f"User {username} was registered correctly.")
            # redirect to a new URL:
            return HttpResponseRedirect(reverse("accounts:login"))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def invite(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = InviteForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            user: User = request.user
            if user.is_anonymous:
                # TODO: It would be nice to be able to forbid an anonymous user to even see this page.
                raise ValidationError("Must be authenticated to invite a user.")
            inviter = User.objects.get(pk=request.user.pk)
            invited_email = form.cleaned_data["invited_email"]

            # Create new invitation in db.
            inviter.inviteduser_set.create(invited_email=invited_email)

            messages.success(request, f"Invitation for {invited_email} saved.")
            # redirect to a new URL:
            return HttpResponseRedirect(reverse("accounts:invite"))
        # else: the render statement at the end of this view will render
        # the form again showing the errors that should be attached to
        # the form in the POST request (?... need to check of course)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = InviteForm()

    return render(request, "accounts/invite.html", {"form": form})
