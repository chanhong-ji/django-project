# Generated by Django 4.1.1 on 2022-11-07 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rooms", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="check_in",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="room",
            name="check_out",
            field=models.TimeField(blank=True, null=True),
        ),
    ]