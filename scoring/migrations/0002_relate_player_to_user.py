# Generated by Django 4.2.2 on 2023-07-08 17:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("scoring", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="player",
            name="name",
        ),
        migrations.AddField(
            model_name="player",
            name="Displayable username accross the app",
            field=models.CharField(
                default=1, max_length=100, verbose_name="displayname"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="player",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
