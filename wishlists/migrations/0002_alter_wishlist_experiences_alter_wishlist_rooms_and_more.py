# Generated by Django 4.1.1 on 2022-11-08 08:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("experiences", "0002_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("rooms", "0004_alter_room_amenities_alter_room_category_and_more"),
        ("wishlists", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wishlist",
            name="experiences",
            field=models.ManyToManyField(
                blank=True, related_name="wishlists", to="experiences.experience"
            ),
        ),
        migrations.AlterField(
            model_name="wishlist",
            name="rooms",
            field=models.ManyToManyField(
                blank=True, related_name="wishlists", to="rooms.room"
            ),
        ),
        migrations.AlterField(
            model_name="wishlist",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="wishlists",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
