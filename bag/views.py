from django.shortcuts import render, redirect


def view_bag(request):
    """View to view the contents of the basket in full"""
    return render(request, "bag/bag.html")


def add_to_bag(request, product_id):
    """View to add products to the basket"""

    weight = int(request.POST.get('weight'))

    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    valid_weights = {30, 100, 300}

    if weight in valid_weights:
        weight = str(weight)
        product_id = str(product_id)
        if product_id in bag:
            if weight in bag[product_id]:
                bag[product_id][weight] += 1
            else:
                bag[product_id][weight] = 1
        else:
            bag[product_id] = {weight: 1}

    request.session['bag'] = bag

    return redirect(redirect_url)
