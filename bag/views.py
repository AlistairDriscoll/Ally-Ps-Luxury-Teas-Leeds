from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from shop.models import Product
from bag.contexts import bag_contents


def view_bag(request):
    """
    View to see the contents of the basket in full.
    Offers free samples based on what's missing from the bag.
    """

    # Get the full context from bag_contents
    context = bag_contents(request)

    bag = request.session.get("bag", [])

    # Get all product IDs the user currently has in the bag
    bag_product_ids = {int(item["product_id"]) for item in bag}

    # Get all tea product IDs in the shop
    all_product_ids = set(Product.objects.values_list("id", flat=True))
    missing_products = list(all_product_ids - bag_product_ids)

    breakfast_blend_sample = None
    sample_or_samples = []

    if len(missing_products) == 0:
        # User has bought one of each tea— offer the big Breakfast Blend sample
        breakfast_blend_sample = (
            Product.objects.filter(name__icontains="Breakfast Blend")
            .values_list("id", flat=True)
            .first()
        )
        if not breakfast_blend_sample:
            messages.warning(request, "Breakfast Blend sample not found.")
    else:
        # Always offer up to 3 teas they don't yet have
        sample_or_samples = Product.objects.filter(id__in=missing_products)[:3]

    # Add to context for template rendering
    context["breakfast_blend_sample"] = breakfast_blend_sample
    context["sample_or_samples"] = sample_or_samples

    return render(request, "bag/bag.html", context)


def add_to_bag(request, product_id):
    """Add a product and weight to the bag session"""
    product = get_object_or_404(Product, pk=product_id)
    weight = int(request.POST.get("weight"))
    redirect_url = request.POST.get("redirect_url")

    # Get or reset bag as a list (ensuring it's not the old dict format)
    bag = request.session.get("bag", [])
    if not isinstance(bag, list):
        bag = []

    # Add new item without merging
    bag.append(
        {
            "product_id": int(product_id),
            "weight": weight,
        }
    )

    request.session["bag"] = bag
    messages.success(request, f"{product.name} ({weight}g) added to your bag.")
    return redirect(redirect_url)


@require_POST
def edit_bag(request, product_id):
    """
    View to allow users to change the weight of a single bag item.
    Quantity is removed; each product+weight is unique.
    """
    product = get_object_or_404(Product, pk=product_id)
    new_weight = int(request.POST.get("weight"))

    bag = request.session.get("bag", [])
    updated_bag = []
    updated = False

    for item in bag:
        if int(item["product_id"]) == int(product_id):
            if not updated:
                updated_bag.append(
                    {
                        "product_id": product_id,
                        "weight": new_weight,
                    }
                )
                updated = True  # Only change one matching item
            else:
                updated_bag.append(item)
        else:
            updated_bag.append(item)

    request.session["bag"] = updated_bag
    request.session.modified = True
    messages.success(request,
                     f"{product.name} weight updated to {new_weight}g.")

    return redirect("view_bag")


def delete_from_bag(request, product_id, weight):
    """Remove a specific product and weight from the bag"""
    product = get_object_or_404(Product, pk=product_id)
    weight = int(weight)

    bag = request.session.get("bag", [])

    # Remove the matching item
    new_bag = []
    sample_removed = False
    for item in bag:
        if int(
            item["product_id"]) == int(product_id) and int(
                item["weight"]) == weight:
            if weight in [5, 20]:
                sample_removed = True
            continue  # Skip this item (we're removing it)
        new_bag.append(item)

    request.session["bag"] = new_bag
    if sample_removed:
        request.session["sample_product_id"] = None

    # Check if 20g Breakfast Blend sample should still be allowed
    current_ids = {int(i["product_id"]) for i in new_bag}
    all_ids = set(Product.objects.values_list("id", flat=True))
    missing_products = list(all_ids - current_ids)

    # If Breakfast Blend 20g exists and no longer qualifies, remove it
    if missing_products:
        filtered = []
        for item in new_bag:
            prod = Product.objects.get(id=item["product_id"])
            if "breakfast blend" in prod.name.lower() and item["weight"] == 20:
                messages.info(
                    request,
                    "You no longer qualify for the 20g"
                    "Breakfast Blend sample, so it was removed.",
                )
                continue  # Skip removing
            filtered.append(item)
        request.session["bag"] = filtered
        request.session["sample_product_id"] = None

    messages.success(request,
                     f"{product.name} ({weight}g) removed from your bag.")
    return redirect("view_bag")
