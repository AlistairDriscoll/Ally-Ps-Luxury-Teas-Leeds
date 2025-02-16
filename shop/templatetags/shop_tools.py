from django import template

register = template.Library()


@register.filter(name='calculate_cost')
def calculate_cost(base_price, quantity):
    """Multiplies a given value by a factor based on the quantity."""

    quantity = int(quantity)

    return base_price * quantity
