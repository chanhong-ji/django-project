# Generated by Django 4.0.8 on 2023-01-23 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={
                'verbose_name_plural': 'Amenities',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('country', models.CharField(default='한국', max_length=50)),
                ('city', models.CharField(default='서울', max_length=80)),
                ('price', models.PositiveIntegerField()),
                ('rooms', models.PositiveIntegerField()),
                ('toilets', models.PositiveIntegerField()),
                ('descriptions', models.TextField(max_length=250)),
                ('address', models.TextField(max_length=250)),
                ('pet_friendly', models.BooleanField(default=False)),
                ('kind', models.CharField(choices=[('entire_place', 'Entire Place'), ('private_room', 'Private Room'), ('shared_room', 'Shared Room')], max_length=50)),
                ('check_in_time', models.TimeField()),
                ('check_out_time', models.TimeField()),
                ('amenities', models.ManyToManyField(blank=True, related_name='rooms', to='rooms.amenity')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rooms', to='categories.category')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
