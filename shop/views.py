from django.shortcuts import render, get_object_or_404

from .models import Product


def shop(request):
    """ View to display the products """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'shop/shop.html', context)


def product_detail(request, sku):
    """ View to display the product details page """

    product = get_object_or_404(Product, sku=sku)

    context = {
        'product': product
    }

    return render(request, 'shop/product_detail.html', context)
