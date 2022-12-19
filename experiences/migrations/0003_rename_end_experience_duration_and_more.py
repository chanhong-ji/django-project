# Generated by Django 4.1.1 on 2022-12-19 08:01

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("experiences", "0002_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="experience",
            old_name="end",
            new_name="duration",
        ),
        migrations.AlterField(
            model_name="experience",
            name="start",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.TimeField(blank=True, null=True), size=5
            ),
        ),
    ]
