# Generated by Django 4.1.3 on 2022-12-16 11:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("twitchapp", "0001_initial"),
        ("streamer", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="streameract",
            name="twitch_account",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                to="twitchapp.twitchaccount",
            ),
        ),
        migrations.AddField(
            model_name="streamer",
            name="user",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
