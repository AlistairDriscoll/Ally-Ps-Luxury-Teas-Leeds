from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import UserProfile


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
