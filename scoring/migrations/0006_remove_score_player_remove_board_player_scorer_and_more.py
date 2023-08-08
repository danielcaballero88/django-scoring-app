# Generated by Django 4.2.2 on 2023-07-23 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("scoring", "0005_player_role"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="score",
            name="player",
        ),
        migrations.RemoveField(
            model_name="board",
            name="player",
        ),
        migrations.CreateModel(
            name="Scorer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                (
                    "board",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="scoring.board"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="score",
            name="scorer",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.RESTRICT,
                to="scoring.scorer",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="board",
            name="player",
            field=models.OneToOneField(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="scoring.player",
            ),
            preserve_default=False,
        ),
    ]
