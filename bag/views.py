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

    bag = request.session.get("bag", {}) or {}

    # turn it into integers
    all_product_ids = set(Product.objects.values_list("id", flat=True))
    bag_product_ids = set(map(int, bag.keys()))

    missing_products = list(all_product_ids - bag_product_ids)

    breakfast_blend_sample = None
    sample_or_samples = []

    # Functionality to get sample products
    if not missing_products:
        breakfast_blend_sample = (
            Product.objects.filter(name__icontains="Breakfast Blend")
            .values_list("id", flat=True)
            .first()
        )
        print(f"Breakfast Blend Sample: {breakfast_blend_sample}")
    elif 1 <= len(missing_products) <= 3:
        sample_or_samples = list(
            Product.objects.filter(id__in=missing_products)[:3])
    else:
        sample_or_samples = list(
            Product.objects.filter(
                id__in=random.sample(
                    missing_products, min(len(missing_products), 3))
            )
        )

    context = {
        "breakfast_blend_sample": breakfast_blend_sample,
        "sample_or_samples": sample_or_samples,
        "weight_options": [30, 100, 300],
    }

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


def delete_from_bag(request, product_id, weight):
    """View to remove a specific product and weight from the bag"""

    bag = request.session.get("bag", {})

    # Convert product_id and weight to strings
    product_id = str(product_id)
    weight = str(weight)

    if product_id in bag:
        if weight in bag[product_id]:
            # Remove the specific weight from the product
            del bag[product_id][weight]

            # If no more weights exist for this product, remove entirely
            if not bag[product_id]:
                del bag[product_id]

            # sample-specific logic (for 5g or 20g weights)
            if weight == "5" or weight == "20":
                print(request.session["sample_product_id"])
                request.session["sample_product_id"] = None

            messages.success(request, "Item removed from your bag.")
        else:
            # If the specific weight isn't found for this product
            messages.error(
                request,
                ("The specified product weight"
                 "is not associated with your bag."),
            )
    else:
        # If the product itself isn't found in the bag
        messages.error(request, "Product not found in your bag.")

    # Update the session with the modified bag
    request.session["bag"] = bag
    request.session.modified = True

    # Redirect the user back to the bag view
    return redirect("view_bag")
