from django.shortcuts import render, get_object_or_404

from .models import Product


def shop(request):
    """ View to display the products """

    tea_type = request.GET.get("type")  # Get selected type from URL parameters

    if tea_type is not None:
        products = Product.objects.filter(tea_type=tea_type)
    else:
        products = Product.objects.all()  # Show all products if no filter

    tea_types = Product.TYPES  # Get available types from the model

    context = {
        'products': products,
        'tea_types': tea_types,
        'selected_type': tea_type,
    }

    return render(request, 'shop/shop.html', context)


def product_detail(request, sku):
    """ View to display the product details page """

    product = get_object_or_404(Product, sku=sku)

    context = {
        'product': product
    }

    return render(request, 'shop/product_detail.html', context)
