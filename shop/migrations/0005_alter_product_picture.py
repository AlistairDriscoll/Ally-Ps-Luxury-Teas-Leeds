# Generated by Django 4.2 on 2025-03-06 16:11

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_product_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='picture',
            field=cloudinary.models.CloudinaryField(blank=True, default='placeholder', max_length=255),
        ),
    ]
