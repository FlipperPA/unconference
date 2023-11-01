# Generated by Django 4.2.6 on 2023-11-01 20:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Room",
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
                ("title", models.TextField()),
                ("description", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="ScheduleTime",
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
                ("title", models.TextField()),
                ("start", models.DateTimeField()),
                ("end", models.DateTimeField()),
                ("allow_sessions", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="UnConferenceEvent",
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
                ("title", models.TextField()),
                ("start", models.DateTimeField()),
                ("end", models.DateTimeField()),
                ("active", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "UnConference event",
            },
        ),
        migrations.CreateModel(
            name="Session",
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
                ("title", models.TextField()),
                ("description", models.TextField()),
                (
                    "session_type",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "Talk"), (2, "Discussion"), (3, "Hands-On")],
                        default=1,
                        help_text="The type of session.",
                    ),
                ),
                ("leaders", models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                (
                    "room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="unconference.room",
                    ),
                ),
                (
                    "schedule_time",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="unconference.scheduletime",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="scheduletime",
            name="unconference_event",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="unconference.unconferenceevent",
            ),
        ),
        migrations.AddField(
            model_name="room",
            name="unconference_event",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="unconference.unconferenceevent",
            ),
        ),
    ]
