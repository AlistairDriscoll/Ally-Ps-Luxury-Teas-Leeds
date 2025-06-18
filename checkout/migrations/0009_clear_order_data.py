from django.db import migrations


def clear_orders_and_items(apps, schema_editor):
    Order = apps.get_model("checkout", "Order")
    OrderItem = apps.get_model("checkout", "OrderItem")

    OrderItem.objects.all().delete()
    Order.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("checkout",
         "0008_alter_order_address_line1_alter_order_postcode_and_more"),
    ]

    operations = [
        migrations.RunPython(clear_orders_and_items),
    ]
