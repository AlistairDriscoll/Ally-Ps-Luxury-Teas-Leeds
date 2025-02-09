from django.shortcuts import render

from .models import Product


def products(request):
    """ View to display the products """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'shop/shop.html', context)
