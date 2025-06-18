from decimal import Decimal
from shop.models import Product


def bag_contents(request):
    """
    Returns context with bag items, total cost, and sample status.
    Assumes each product+weight combo is added once, no quantity.
    """

    bag = request.session.get("bag", {})
    bag_items = []
    total = Decimal("0.00")
    total_items = 0
    sample_added = False
    sample_product = None

    for product_id, weights in bag.items():
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            continue

        for weight_str in weights:
            weight = int(weight_str)

            if weight in [5, 20]:
                price = Decimal("0.00")
                sample_added = True
                sample_product = product
            elif weight == 30:
                price = product.base_price_number
                total += price
                total_items += 1
            elif weight == 100:
                price = product.base_price_number * 3
                total += price
                total_items += 1
            elif weight == 300:
                price = product.base_price_number * 8
                total += price
                total_items += 1
            else:
                # Catch-all fallback (shouldn’t really happen)
                price = product.base_price_number
                total += price
                total_items += 1

            bag_items.append(
                {
                    "product": product,
                    "weight": weight,
                    "price": price,
                }
            )

    context = {
        "bag_items": bag_items,
        "total": total,
        "total_items": total_items,
        "sample_added": sample_added,
        "sample_product": sample_product,
    }

    return context
