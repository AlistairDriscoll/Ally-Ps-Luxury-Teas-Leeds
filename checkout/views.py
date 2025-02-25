from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

from .forms import OrderForm
from .models import OrderItem, Order
from shop.models import Product
from profiles.models import UserProfile

import json


def checkout(request):
    """View for the checkout"""

    if request.method == "POST":
        bag = request.session.get("bag", {})
        save_info = request.POST("save_info")

        form_data = {
            "full_name": request.POST["full_name"],
            "email": request.POST["email"],
            "phone_number": request.POST["phone_number"],
            "country": request.POST["country"],
            "postcode": request.POST["postcode"],
            "town_or_city": request.POST["town_or_city"],
            "address_line1": request.POST["address_line1"],
            "address_line2": request.POST["address_line2"],
            "state_or_region": request.POST["state_or_region"],
        }

        order_form = OrderForm(form_data)

        if order_form.is_valid():
            if request.user.is_authenticated:
                profile = get_object_or_404(UserProfile, user=request.user)
                if save_info:
                    profile.full_name = form_data['full_name']
                    profile.email = form_data['email']
                    profile.phone_number = form_data['phone_number']
                    profile.country = form_data['country']
                    profile.postal_code = form_data['postcode']
                    profile.town_or_city = form_data['town_or_city']
                    profile.address_line1 = form_data['address_line1']
                    profile.address_line2 = form_data['address_line2']
                    profile.state_or_region = form_data['state_or_region']
                    profile.save()

            order = order_form.save(commit=False)
            order.original_bag = json.dumps(bag)
            order.save()
            for item_id, weights in bag.items():
                try:
                    product = Product.objects.get(pk=item_id)
                    for weight, quantity in weights.items():
                        order_item = OrderItem(
                            order=order,
                            product=product,
                            weight=weight,
                            quantity=quantity
                        )
                        order_item.save()
                except Product.DoesNotExist:
                    messages.error(
                        request,
                        "One of your products doesn't exist in our database!"
                        "Please contact us for further information."
                    )
                    order.delete()
                    return redirect(reverse("view_bag"))

            order.save()

            context = {
                'order': order,
            }
            return redirect(reverse("payment", args=[order.id]))
        else:
            messages.error(
                request,
                """There was an error with your form.
                Please double check your information.""",
            )
    else:
        bag = request.session.get('bag', {})

        if not bag:
            messages.error(request, "There is nothing in your bag!")
            return redirect(reverse('shop'))

        order_form = OrderForm()
        template = 'checkout/checkout.html'
        context = {
            "order_form": order_form,
        }

        return render(request, template, context)


def checkout_success(request, order_id):
    """Renders the payment section of the form"""

    if request.method == "GET":
        order = get_object_or_404(Order, pk=order_id)

    context = {
        'order': order,
        "stripe_public_key": """pk_test_51QPRXqGHaqkD0AzD6fypQbKMWij5eQ1RMRVys8
        kd4Tyj9TxwAfmM1dpoiCNXQ2tCbPCbtGeIpW761yBFeW3ll1bF00CrFQHp3G""",
        "client_secret": "Test client secret",
    }

    return render(request, 'checkout/payment.html', context)
