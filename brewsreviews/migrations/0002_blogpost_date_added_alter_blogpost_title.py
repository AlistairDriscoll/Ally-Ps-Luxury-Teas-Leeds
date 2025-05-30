# Generated by Django 4.2 on 2025-03-04 23:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('brewsreviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='title',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
