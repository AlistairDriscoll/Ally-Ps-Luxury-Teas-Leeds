# Generated by Django 4.2 on 2025-02-07 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='city',
            new_name='town_or_city',
        ),
    ]
