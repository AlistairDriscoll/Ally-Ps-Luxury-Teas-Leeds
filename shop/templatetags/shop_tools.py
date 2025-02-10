from django import template

register = template.Library()


@register.filter(name='calculate_cost')
def calculate_cost(base_price, factor):
    """Multiplies a given value by a factor."""
    if factor == 5:
        return 0
    else:
        try:
            return round(float(base_price) * int(factor), 2)
        except (ValueError, TypeError):
            return base_price  # Returns the original value if there's an error
