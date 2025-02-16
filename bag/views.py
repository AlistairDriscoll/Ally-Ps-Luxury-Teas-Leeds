from django.shortcuts import render, redirect
from django.contrib import messages


def view_bag(request):
    """
    View to view the contents of the basket in full
    Gets a list of what samples the customer hasn't ordered
    If they have ordered everything then add 5g of a random tea
    """

    return render(request, "bag/bag.html")


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
