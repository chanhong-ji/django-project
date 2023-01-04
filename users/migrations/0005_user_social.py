# Generated by Django 4.1.1 on 2023-01-03 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_user_avatar"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="social",
            field=models.CharField(
                blank=True,
                choices=[("kakao", "Kakao"), ("github", "Github")],
                max_length=6,
                null=True,
            ),
        ),
    ]
