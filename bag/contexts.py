from django.shortcuts import get_object_or_404
from shop.models import Product


def bag_contents(request):
    """
    For storing bag contents
    and providing context without modifying the session.
    New version for list-style bag entries.
    """

    bag = request.session.get("bag", [])
    sample_product_id = request.session.get("sample_product_id")
    sample_added = False

    bag_items = []
    total = 0
    total_items = 0
    sample_product = None

    for item in bag:
        product_id = item.get("product_id")
        weight = int(item.get("weight"))

        product = Product.objects.filter(id=product_id).first()
        if not product:
            continue

        # Pricing logic
        if weight in [5, 20]:
            price = 0
            sample_added = True
            if weight == 5:
                request.session["sample_product_id"] = product_id
        elif weight == 30:
            price = product.base_price_number
        elif weight == 100:
            price = product.base_price_number * 3
        elif weight == 300:
            price = product.base_price_number * 8
        else:
            price = 0  # Fallback safeguard

        bag_items.append(
            {
                "product": product,
                "weight": weight,
                "price": round(price, 2),
                "subtotal": round(price, 2),
            }
        )

        total += price
        total_items += 1

    # Handle sample appearance if it should still show up
    if sample_product_id and not any(
        item["product"].id == sample_product_id and item["weight"] == 5
        for item in bag_items
    ):
        sample_product = get_object_or_404(Product, id=sample_product_id)
        bag_items.append(
            {
                "product": sample_product,
                "weight": 5,
                "price": 0,
                "subtotal": 0,
            }
        )
        total_items += 1
        sample_added = True

    total = round(total, 2)

    context = {
        "bag_items": bag_items,
        "total_items": total_items,
        "total": total,
        "sample_added": sample_added,
        "sample_product": sample_product,
    }

    return context
