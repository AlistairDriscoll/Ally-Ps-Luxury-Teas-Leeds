# <project>/<app>/management/commands/seed.py
from django.core.management.base import BaseCommand

from shop.models import Product

# python manage.py seed --mode=refresh

""" Clear all data and creates addresses """
MODE_REFRESH = "refresh"

""" Clear all data and do not create any object """
MODE_CLEAR = "clear"


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument("--mode", type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write("seeding data...")
        run_seed(self, options["mode"])
        self.stdout.write("done.")


def clear_data():
    """Deletes all the table data"""
    print("Delete Product instances")
    Product.objects.all().delete()


def create_product():
    """Creates an address object combining different elements from the list"""

    current_tea_list = [
        "Breakfast Blend",
        "Afternoon Blend",
        "Earl Grey",
        "Ginger Beer",
        "Grapefruit Green",
        "Lover's Leap",
        "Mojitea",
        "Moroccan Mint Green",
        "Rose Earl Grey",
        "Rose Petal",
    ]

    def choose_base_price(name):
        if name == "Breakfast Blend":
            return 2.5
        elif name == "Afternoon Blend" or "Lover's Leap" or "Earl Grey":
            return 3
        elif name == "Moroccan Mint Green" or "Mojitea" or "Grapefruit Green":
            return 3.5
        else:
            return 4

    for tea in current_tea_list:

        product = Product(
                    name=tea,
                    base_price_number=choose_base_price(tea)
                    )

        product.save()

    return product


def run_seed(self, mode):
    """Seed database based on mode

    :param mode: refresh / clear
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    # Creating 15 addresses
    for i in range(10):
        create_product()
