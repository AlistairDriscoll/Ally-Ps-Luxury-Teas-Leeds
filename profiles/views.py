from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
    order_items = order.order_items

    # checks to see if order belongs to current user
    if request.user.pk != order.user_profile.user.pk:
        messages.error(request, 'Apologies, but you cannot view this order!')
        return redirect('profile')

    context = {
        'order_items': order_items,
        'order': order,
    }

    return render(request, 'profiles/view_order.html', context)


@login_required
def edit_profile(request):
    """View for presenting the user details form"""

    user_profile_form = UserProfileForm

    context = {
        'form': user_profile_form,
    }

    return render(request, 'profiles/edit_form.html', context)
