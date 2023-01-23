# Generated by Django 4.0.8 on 2023-01-23 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('kind', models.CharField(choices=[('room', 'Room'), ('experience', 'Experience')], max_length=15)),
                ('check_in', models.DateField(blank=True, null=True)),
                ('check_out', models.DateField(blank=True, null=True)),
                ('experience_date', models.DateField(blank=True, null=True)),
                ('guests', models.PositiveIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
