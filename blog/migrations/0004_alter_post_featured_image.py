# Generated by Django 3.2.13 on 2022-06-18 18:51

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_post_featured_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='featured_image',
            field=cloudinary.models.CloudinaryField(default='https://res.cloudinary.com/roibeard/image/upload/v1655578160/placeholder.jpg', max_length=255, verbose_name='image'),
        ),
    ]
