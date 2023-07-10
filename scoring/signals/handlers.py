from ..models import Player


def create_player_profile(sender, **kwargs):
    print("signal sent by ", sender, kwargs)
    # Create player profile for the newly registered user.
    user = kwargs.get("user")
    if not user:
        raise ValueError("Missing user in the kwargs.")

    Player(
        displayname=user.username,
        user=user,
    ).save()
