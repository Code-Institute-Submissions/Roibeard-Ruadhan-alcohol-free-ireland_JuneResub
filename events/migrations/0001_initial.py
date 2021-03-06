# Generated by Django 3.2.13 on 2022-06-18 19:29

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=150)),
                ('venue', models.CharField(max_length=150)),
                ('venue_image', cloudinary.models.CloudinaryField(default='placeholder', max_length=255, verbose_name='image')),
                ('event_date', models.DateField(blank=True, null=True, verbose_name='Event Date')),
                ('description', models.TextField(blank=True, max_length=200)),
                ('approve', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events_creator', to=settings.AUTH_USER_MODEL)),
                ('guests', models.ManyToManyField(blank=True, related_name='events_guests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Event',
            },
        ),
    ]
