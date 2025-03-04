import random

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
    }

    return render(request, "bag/bag.html", context)


def add_to_bag(request, product_id):
    """View to add products to the basket"""

    weight = int(request.POST.get("weight"))
    redirect_url = request.POST.get("redirect_url")
    sample_added = request.POST.get("sample_added")
    bag = request.session.get("bag", {})

    valid_weights = {5, 30, 100, 300}

    if weight in valid_weights:
        if weight == 5 and sample_added is False:
            sample_added = True
        elif weight == 5 and sample_added is True:
            messages.warning(
                request, "You have already added a sample to your bag!"
                )
            return render(request, "bag/bag.html")
        messages.success(request, "Added to your Bag!")
        weight = str(weight)
        product_id = str(product_id)
        if product_id in bag:
            if weight in bag[product_id]:
                bag[product_id][weight] += 1
            else:
                bag[product_id][weight] = 1
        else:
            bag[product_id] = {weight: 1}
    else:
        messages.error(request, "You need to select a compatible weight!")
        return render(request, 'shop/shop.html')

    request.session["bag"] = bag

    return redirect(redirect_url)
