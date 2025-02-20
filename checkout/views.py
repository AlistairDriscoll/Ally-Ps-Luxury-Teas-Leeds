from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    """View for the checkout"""

    bag = request.session.get('bag', {})

    if not bag:
        messages.error(request, "There is nothing in your bag!")
        return redirect(reverse('products'))

    order_form = OrderForm
    template = 'checkout/checkout.html'
    context = {
        "order_form": order_form,
    }

    return render(request, template, context)


def payment(request):
    """Renders the payment section of the form"""

    context = {
        "stripe_public_key": """pk_test_51QPRXqGHaqkD0AzD6fypQbKMWij5eQ1RMRVys8
        kd4Tyj9TxwAfmM1dpoiCNXQ2tCbPCbtGeIpW761yBFeW3ll1bF00CrFQHp3G""",
        "client_secret": "Test client secret",
    }

    return render(request, 'checkout/payment.html', context)
