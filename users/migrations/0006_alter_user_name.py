# Generated by Django 4.1.1 on 2023-01-05 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_user_social"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]