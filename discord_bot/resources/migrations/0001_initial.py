# Generated by Django 3.2 on 2021-04-17 03:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DiscordUser",
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
                ("nickname", models.CharField(max_length=200)),
                ("discord_id", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Feature",
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
                ("name", models.CharField(db_index=True, max_length=100, unique=True)),
                ("value", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="ResourceType",
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
                ("name", models.CharField(max_length=200)),
                ("channel_id", models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="Resource",
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
                ("text", models.TextField()),
                ("tags", models.TextField()),
                (
                    "discord_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="resources.discorduser",
                    ),
                ),
                (
                    "resource_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="resources.resourcetype",
                    ),
                ),
            ],
        ),
    ]
