import random

from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.contrib import messages

from shop.models import Product


def view_bag(request):
    """
    View to see the contents of the basket in full.
    Gets a list of missing products.
    If they have ordered everything, offer 20g of Breakfast Blend.
    Otherwise, offer 5g of up to 3 missing teas for the user to choose from.
    """

    bag = request.session.get("bag", {})

    # turn it into integers
    all_product_ids = set(Product.objects.values_list("id", flat=True))
    bag_product_ids = set(map(int, bag.keys()))

    missing_products = list(all_product_ids - bag_product_ids)

    breakfast_blend_sample = None
    sample_or_samples = []

    # functionality to get sample products
    if not missing_products:
        breakfast_blend_sample = (
            Product.objects.filter(name="Breakfast Blend")
            .values_list("id", flat=True)
            .first()
        )
    elif 1 <= len(missing_products) <= 3:
        sample_or_samples = list(
            Product.objects.filter(id__in=missing_products)[:3])
    else:
        sample_or_samples = list(
            Product.objects.filter(id__in=random.sample(missing_products, 3)))

    context = {
        "breakfast_blend_sample": breakfast_blend_sample,
        "sample_or_samples": sample_or_samples,
        "weight_options": [30, 100, 300],
    }

    return render(request, "bag/bag.html", context)


def add_to_bag(request, product_id):
    """View to add products to the basket"""

    weight = int(request.POST.get("weight"))
    redirect_url = request.POST.get("redirect_url", "view_bag")
    # makes it a boolean value
    is_sample = request.POST.get("is_sample") == "true"
    bag = request.session.get("bag", {})

    valid_weights = {5, 20, 30, 100, 300}

    # Ensure sample tracking exists in the session
    if "sample_added" not in request.session:
        request.session["sample_added"] = False

    if weight in valid_weights:
        if is_sample:
            if request.session["sample_added"]:
                messages.warning(
                    request, "You have already claimed a free sample!")
                return redirect("view_bag")

            request.session["sample_added"] = True
            request.session["sample_product_id"] = product_id

        # Add product to bag
        weight = str(weight)
        product_id = str(product_id)

        if product_id in bag:
            if weight in bag[product_id]:
                bag[product_id][weight] += 1
            else:
                bag[product_id][weight] = 1
        else:
            bag[product_id] = {weight: 1}

        messages.success(request, "Added to your Bag!")

    else:
        messages.error(request, "You need to select a compatible weight!")
        return redirect("shop")

    request.session["bag"] = bag
    request.session.modified = True

    return redirect(redirect_url)


@require_POST
def edit_bag(request, product_id):
    """
    View to enable the user to edit the quantity and amount of each bag item
    """

    new_weight = request.POST.get("weight")
    new_quantity = int(request.POST.get("quantity", 0))
    bag = request.session.get('bag', {})

    product_id = str(product_id)
    # If weight has changed, remove old weight and replace with the new one
    if product_id in bag:
        if new_weight in bag[product_id]:
            # Update the quantity or weight
            if new_quantity > 0:
                bag[product_id][new_weight] = new_quantity
                messages.success(request, "Bag updated successfully!")
            else:
                del bag[product_id][new_weight]
                messages.success(request, "Weight removed from your bag!")

                # If no weights remain for this product, remove entirely
                if not bag[product_id]:
                    del bag[product_id]
                    messages.success(request, "Item removed from your bag!")

        else:
            messages.error(
                request, "Weight not found for this product in your bag!")

        request.session["bag"] = bag
        request.session.modified = True
    else:
        messages.error(request, "Item not found in your bag!")

    return redirect("view_bag")
