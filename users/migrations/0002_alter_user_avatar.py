# Generated by Django 4.1.1 on 2022-11-17 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.URLField(blank=True),
        ),
    ]