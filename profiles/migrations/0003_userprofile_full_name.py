# Generated by Django 4.2 on 2025-02-16 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_rename_city_userprofile_town_or_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='full_name',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
