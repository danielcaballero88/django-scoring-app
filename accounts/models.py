from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class InvitedUser(models.Model):
    inviter = models.ForeignKey(User, on_delete=models.CASCADE)
    invited_email = models.EmailField("Invited user email.", max_length=100)

    def __str__(self):
        return f"{self.invited_email} invited by {self.inviter.username}"
