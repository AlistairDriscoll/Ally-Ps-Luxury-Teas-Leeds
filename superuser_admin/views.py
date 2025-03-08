from django.shortcuts import render, redirect
from django.contrib import messages
from checkout.models import Order
from about.models import Enquiry


def superuser_admin_page(request):
    """Renders the superuser admin page"""

    if not request.user.is_superuser:
        messages.warning(request, "You are not allowed to visit this page")
        return redirect('shop')
    else:
        orders = Order.objects.all()
        enquiries = Enquiry.objects.all()
        context = {
            'orders': orders,
            'enquiries': enquiries,
        }
        return render(request, 'superuser_admin/admin.html', context)
