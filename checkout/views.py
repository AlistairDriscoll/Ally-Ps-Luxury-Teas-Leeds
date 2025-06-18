from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .forms import OrderForm
from .models import OrderItem, Order
from shop.models import Product
from profiles.models import UserProfile
from bag.contexts import bag_contents

import json
import stripe


@login_required
def checkout(request):
    """View for the checkout"""
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == "POST":
        bag = request.session.get("bag", [])
        save_info = request.POST.get("save_info", False)

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
                    profile.full_name = form_data["full_name"]
                    profile.email = form_data["email"]
                    profile.phone_number = form_data["phone_number"]
                    profile.country = form_data["country"]
                    profile.postal_code = form_data["postcode"]
                    profile.town_or_city = form_data["town_or_city"]
                    profile.address_line1 = form_data["address_line1"]
                    profile.address_line2 = form_data["address_line2"]
                    profile.state_or_region = form_data["state_or_region"]

                subscribed_checkbox = request.POST.get(
                    "subscribed_to_email") == "on"
                profile.subscribed_to_email = subscribed_checkbox
                profile.save()

            order = order_form.save(commit=False)
            order.user_profile = profile
            order.original_bag = json.dumps(bag)
            order.save()

            for item in bag:
                try:
                    product = Product.objects.get(pk=item["product_id"])
                    weight = item["weight"]

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        weight=weight,
                    )
                except Product.DoesNotExist:
                    messages.warning(
                        request,
                        "A product in your bag no longer exists."
                        " Please contact us.",
                    )
                    order.delete()
                    return redirect("view_bag")

            order.save()
            return redirect(
                "checkout_success", order_number=order.order_number)

        else:
            messages.error(
                request,
                "There was an error with your form."
                " Please double-check your information.",
            )

    else:
        bag = request.session.get("bag", [])

        if not bag:
            messages.error(request, "There is nothing in your bag!")
            return redirect(reverse("shop"))

        current_bag = bag_contents(request)
        bag_total = current_bag["total"]
        stripe_total = round(bag_total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        user_profile = getattr(request.user, "user_profile", None)
        subscribed_to_email = (
            user_profile.subscribed_to_email
            if request.user.is_authenticated and user_profile
            else False
        )

        initial_data = {
            "full_name": getattr(user_profile, "full_name", ""),
            "email": getattr(user_profile, "email", ""),
            "phone_number": getattr(user_profile, "phone_number", ""),
            "address_line1": getattr(user_profile, "address_line1", ""),
            "address_line2": getattr(user_profile, "address_line2", None),
            "town_or_city": getattr(user_profile, "town_or_city", ""),
            "state_or_region": getattr(user_profile, "state_or_region", ""),
            "country": getattr(user_profile, "country", ""),
            "postcode": getattr(user_profile, "postal_code", ""),
        }

        order_form = OrderForm(initial=initial_data)

    template = "checkout/checkout.html"
    context = {
        "order_form": order_form,
        "stripe_public_key": stripe_public_key,
        "client_secret": intent.client_secret,
        "subscribed_to_email": subscribed_to_email,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Displays once successful checkout is made
    """
    order = get_object_or_404(Order, order_number=order_number)

    if order.delivery_cost == 3:
        messages_time = "two days time."
    elif order.delivery_cost == 7:
        messages_time = "one week's time."
    else:
        messages_time = "two weeks' time."

    messages.success(
        request,
        f"We have received your order for processing! "
        f"Your order will arrive in {messages_time}",
    )

    # Clear updated list-based bag session
    request.session.pop("bag", None)
    request.session.pop("sample_product_id", None)
    request.session.modified = True

    context = {
        "order": order,
    }

    return render(request, "checkout/checkout_success.html", context)


def checkout_with_sample(request, pk):
    """
    Handles checkout when a user selects a free sample.
    """
    bag = request.session.get("bag", [])

    if not bag:
        messages.error(request, "There is nothing in your bag!")
        return redirect(reverse("shop"))

    sample_product = get_object_or_404(Product, pk=pk)

    # Check if a sample has already been added
    if "sample_product_id" in request.session:
        messages.warning(request, "You have already claimed a free sample!")
        return redirect("view_bag")

    # Add the sample item to the bag
    sample_item = {
        "product_id": sample_product.id,
        "weight": "5",
    }

    bag.append(sample_item)
    request.session["bag"] = bag
    request.session["sample_product_id"] = pk
    request.session.modified = True

    messages.success(
        request,
        f"Your order now includes a free 5g sample of {sample_product}!",
    )

    return redirect("checkout")
