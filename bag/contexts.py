from django.shortcuts import get_object_or_404

from shop.models import Product


def bag_contents(request):
    """
    For storing bag contents
    and providing context without modifying the session.
    """

    bag = request.session.get("bag", {})
    sample_product_id = request.session.get("sample_product_id")
    sample_added = bool(sample_product_id)

    bag_items = []
    total = 0
    total_items = 0

    for item_id, weights in bag.items():
        products = Product.objects.all()
        product = products.filter(id=item_id).first()

        for weight, quantity in weights.items():
            weight = int(weight)
            total_items += quantity
            if weight == 5:
                price = 0
            elif weight == 30:
                price = product.base_price_number
            elif weight == 100:
                price = product.base_price_number * 3
            elif weight == 300:
                price = product.base_price_number * 8

            total += price * quantity
            bag_items.append(
                {
                    "product": product,
                    "weight": weight,
                    "quantity": quantity,
                    "price": round(price, 2),
                    "subtotal": round(price * quantity, 2),
                }
            )

    if sample_added:
        sample_product = get_object_or_404(Product, id=sample_product_id)
        bag_items.append(
            {
                "product": sample_product,
                "weight": 5,
                "quantity": 1,
                "price": 0,
                "subtotal": 0,
            }
        )
        total_items += 1

    total = round(total, 2)

    context = {
        "bag_items": bag_items,
        "total_items": total_items,
        "total": total,
        "sample_added": sample_added,
        "sample_product": sample_product if sample_added else None,
    }
    return context
