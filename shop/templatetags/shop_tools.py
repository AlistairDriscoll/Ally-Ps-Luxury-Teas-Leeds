from django import template

register = template.Library()


@register.filter(name='calculate_cost')
def calculate_cost(base_price, factor):
    """Multiplies a given value by a factor."""

    return base_price * factor
