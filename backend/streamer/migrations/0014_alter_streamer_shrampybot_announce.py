# Generated by Django 4.1.3 on 2022-12-13 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamer', '0013_rename_streamergsgfile_streameract_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamer',
            name='shrampybot_announce',
            field=models.BooleanField(default=True),
        ),
    ]