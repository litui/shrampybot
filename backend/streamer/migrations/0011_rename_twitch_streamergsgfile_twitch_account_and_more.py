# Generated by Django 4.1.3 on 2022-12-10 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streamer', '0010_streamer_og_shramp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='streamergsgfile',
            old_name='twitch',
            new_name='twitch_account',
        ),
        migrations.RenameField(
            model_name='streamermastodon',
            old_name='twitch',
            new_name='twitch_account',
        ),
    ]