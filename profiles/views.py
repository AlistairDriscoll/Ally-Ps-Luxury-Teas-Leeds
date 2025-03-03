from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .models import UserProfile
from checkout.models import Order
from .forms import UserProfileForm


@login_required
def profile(request):
    """ Profile view """

    profile = get_object_or_404(UserProfile, user=request.user)
    user_orders = profile.orders.all()

    context = {
        'profile': profile,
        'orders': user_orders,
    }

    return render(request, 'profiles/profile.html', context)


@login_required
def view_order(request, order_number):
    """
    View for the user to see an individual order in full
    """

    order = get_object_or_404(Order, order_number=order_number)
    order_items = order.lineitems.all()

    # checks to see if order belongs to current user
    if request.user.pk != order.user_profile.user.pk:
        messages.error(request, 'Apologies, but you cannot view this order!')
        return redirect('shop')

    context = {
        'order_items': order_items,
        'order': order,
    }

    return render(request, 'profiles/view_order.html', context)


@login_required
def edit_profile(request, userkey):
    """View for presenting the user details form"""

    try:
        userkey = int(userkey)
    except ValueError:
        messages.error(request, "Invalid user profile.")
        return redirect("shop")

    user_profile = get_object_or_404(UserProfile, user__id=userkey)
    if request.user.pk != userkey:
        messages.warning(request, 'You cannot view that profile!')
        return redirect('shop')

    if request.method == "POST":
        user_profile_form = UserProfileForm(
            request.POST, instance=user_profile)
        if user_profile_form.is_valid():
            user_profile_form.save()
            subscribed_to_email = request.POST.get(
                'subscribed_to_email') == 'on'
            user_profile.subscribed_to_email = subscribed_to_email
            user_profile.save()
        else:
            messages.error(
                request,
                ("There was an error processing your details,"
                 "please contact us!"),
            )
    else:
        user_profile_form = UserProfileForm(instance=user_profile)

    context = {
        'form': user_profile_form,
        'user_profile': user_profile,
    }

    return render(request, 'profiles/edit_form.html', context)


@login_required
def account_deletion(request, userkey):
    """
    Will take the user to a page where they can delete their account
    """

    try:
        userkey = int(userkey)
    except ValueError:
        messages.error(request, "Invalid user profile.")
        return redirect("shop")

    if request.user.pk != userkey:
        messages.error(request, "Apologies, but you cannot view this page!")
        return redirect("shop")

    user = get_object_or_404(User, pk=userkey)

    if request.method == 'POST':
        user.delete()
        messages.info(request, 'Your profile has now been deleted.')
        return redirect('shop')
    else:
        context = {
            'user': user
        }

        return render(request, 'profiles/account_deletion.html', context)
