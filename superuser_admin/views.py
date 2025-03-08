from django.shortcuts import render, redirect
from django.contrib import messages

from shop.models import Product
from checkout.models import Order
from about.models import Enquiry
from brewsreviews.models import BlogPost
from .forms import BlogPostForm


def superuser_admin_page(request):
    """Renders the superuser admin page"""
    print("Request made, rendering...")
    if not request.user.is_superuser:
        print("Redirecting to shop")
        messages.warning(request, "You are not allowed to visit this page")
        return redirect('shop')
    else:
        print("User is superuser")
        orders = Order.objects.all()
        enquiries = Enquiry.objects.all()
        products = Product.objects.all()
        blog_posts = BlogPost.objects.all()

        context = {
            'orders': orders,
            'enquiries': enquiries,
            'products': products,
            'blog_posts': blog_posts,
        }

        return render(
            request, "superuser_admin/admin.html", context
        )


def manage_post(request, post_pk):
    """View for superuser management of blog posts"""

    post = BlogPost.objects.filter(pk=post_pk)
    form = BlogPostForm(post)

    context = {
        'post': post,
        'form': form
    }

    return render(request, 'superuser_admin/manage_post.html', context)
