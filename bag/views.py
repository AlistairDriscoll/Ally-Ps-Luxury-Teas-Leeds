from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.contrib import messages
from shop.models import Product


def view_bag(request):
    """
    View to see the contents of the basket in full.
    Offers free samples based on what's missing from the bag.
    """

    bag = request.session.get("bag", {}) or {}

    # Calculate missing products (to decide sample eligibility)
    all_product_ids = set(Product.objects.values_list("id", flat=True))
    bag_product_ids = set(map(int, bag.keys()))
    missing_products = list(all_product_ids - bag_product_ids)

    breakfast_blend_sample = None
    sample_or_samples = []

    # Offer correct free sample
    if not missing_products:
        breakfast_blend_sample = (
            Product.objects.filter(name__icontains="Breakfast Blend")
            .values_list("id", flat=True)
            .first()
        )
        if not breakfast_blend_sample:
            messages.warning(request, "Breakfast Blend sample not found.")
    elif 1 <= len(missing_products) <= 3:
        sample_or_samples = Product.objects.filter(id__in=missing_products)[:3]

    # Price multipliers by weight
    weight_multipliers = {
        5: 0,
        20: 0,
        30: 1,
        100: 3,
        300: 8,
    }

    context = {
        "bag_items": [],
        "total": 0,
        "product_count": 0,
        "breakfast_blend_sample": breakfast_blend_sample,
        "sample_or_samples": sample_or_samples,
    }

    # Build up the bag display
    for item_id, weights in bag.items():
        try:
            product = Product.objects.get(id=item_id)
            for weight, quantity in weights.items():
                weight = int(weight)
                multiplier = weight_multipliers.get(weight, 0)
                base_price = product.base_price_number
                item_total = quantity * base_price * multiplier

                context["bag_items"].append(
                    {
                        "product": product,
                        "weight": weight,
                        "quantity": quantity,
                        "item_total": item_total,
                    }
                )

                context["total"] += item_total
                if weight not in [5, 20]:
                    context["product_count"] += quantity
        except Product.DoesNotExist:
            messages.warning(request, f"Product ID {item_id} not found.")
            continue

    return render(request, "bag/bag.html", context)


def add_to_bag(request, product_id):
    """View to add products to the basket"""

    # Retrieve input data
    weight = int(request.POST.get("weight"))
    redirect_url = request.POST.get("redirect_url", "view_bag")
    is_sample = request.POST.get("is_sample") == "true"

    # Retrieve session data
    sample_product_id = request.session.get("sample_product_id")
    bag = request.session.get("bag", {})

    # Validate weight
    valid_weights = {5, 20, 30, 100, 300}
    if weight not in valid_weights:
        messages.error(request, "You need to select a compatible weight!")
        return redirect("shop")

    # Sample-specific logic
    if is_sample:
        if sample_product_id:
            # Prevent duplicate free samples
            messages.warning(request,
                             "You have already claimed a free sample!")
            return redirect("view_bag")
        # Add the sample
        request.session["sample_product_id"] = product_id

    # Convert weight and product_id to strings
    weight = str(weight)
    product_id = str(product_id)

    # Add the product and weight to the bag
    if product_id in bag:
        if weight in bag[product_id]:
            bag[product_id][weight] += 1  # Increment quantity
        else:
            bag[product_id][weight] = 1  # Add weight
    else:
        bag[product_id] = {weight: 1}  # Add new product

    # Save the updated bag and session
    request.session["bag"] = bag
    request.session.modified = True

    # Success message
    messages.success(request, "Added to your Bag!")
    return redirect(redirect_url)


@require_POST
def edit_bag(request, product_id):
    """
    View to enable the user to edit the weight and quantity of each bag item
    """
    new_weight = request.POST.get("weight")
    new_quantity = int(
        request.POST.get("quantity", 1)
    )  # Get quantity, default to 1 if not specified
    bag = request.session.get("bag", {})

    product_id = str(product_id)

    if product_id in bag:
        if new_weight in bag[product_id]:
            # If the weight is already in the bag, update the quantity
            bag[product_id][new_weight] = new_quantity
            messages.success(request, "Bag updated successfully!")
        else:
            # If the weight isn't already in the bag, add it
            current_weights = bag[product_id]
            if current_weights:
                old_weight, old_quantity = list(current_weights.items())[0]
                bag[product_id][new_weight] = new_quantity
                del bag[product_id][old_weight]
            messages.success(request, "Bag updated successfully!")

        # Save changes
        request.session["bag"] = bag
        request.session.modified = True
    else:
        messages.error(request, "Item not found in your bag!")

    return redirect("view_bag")


def delete_from_bag(request, product_id, weight):
    """View to remove a specific product and weight from the bag"""

    bag = request.session.get("bag", {})

    product_id = str(product_id)
    weight = str(weight)

    if product_id in bag:
        if weight in bag[product_id]:
            del bag[product_id][weight]

            if not bag[product_id]:
                del bag[product_id]

            if weight in ["5", "20"]:
                request.session["sample_product_id"] = None

            messages.success(request, "Item removed from your bag.")
        else:
            messages.error(
                request,
                ("The specified product weight "
                 "is not associated with your bag."),
            )
    else:
        messages.error(request, "Product not found in your bag.")

    # Check if user still qualifies for 20g sample
    all_product_ids = set(Product.objects.values_list("id", flat=True))
    bag_product_ids = set(map(int, bag.keys()))
    missing_products = list(all_product_ids - bag_product_ids)

    # If they're now missing any teas, remove 20g Breakfast Blend if in bag
    for item_id, weights in list(bag.items()):
        try:
            product = Product.objects.get(id=item_id)
            if "breakfast blend" in product.name.lower() and "20" in weights:
                if missing_products:
                    del weights["20"]
                    if not weights:
                        del bag[item_id]
                    messages.info(
                        request,
                        "You no longer qualify for the 20g Breakfast"
                        " Blend sample, so it was removed.",
                    )
        except Product.DoesNotExist:
            continue

    request.session["bag"] = bag
    request.session.modified = True
    return redirect("view_bag")
