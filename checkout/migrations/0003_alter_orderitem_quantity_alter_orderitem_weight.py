# Generated by Django 4.2 on 2025-02-16 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_rename_county_order_state_or_region_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='weight',
            field=models.CharField(blank=True, default=30, max_length=3),
        ),
    ]
