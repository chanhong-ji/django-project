# Generated by Django 4.1.1 on 2022-12-28 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("medias", "0005_alter_photo_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="photo",
            name="thumb",
            field=models.BooleanField(default=False),
        ),
    ]
