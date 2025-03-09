from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from shop.models import Product
from checkout.models import Order
from about.models import Enquiry
from brewsreviews.models import BlogPost
from .forms import BlogPostForm


@login_required
def superuser_admin_page(request):
    """Renders the superuser admin page"""

    if not request.user.is_superuser:
        print("Redirecting to shop")
        messages.warning(request, "You are not allowed to visit this page")
        return redirect('shop')
    else:
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


@login_required
def add_post(request):
    """View for the superuser to add a blog post"""

    if request.user.is_superuser:
        if request.method == "GET":
            form = BlogPostForm()

            context = {
                'form': form
            }

            return render(request, "superuser_admin/add_post.html", context)

        else:
            blog_post_form = BlogPostForm(request.POST)

            if blog_post_form.is_valid():
                blog_post_form.save()
                messages.success(request, 'Blog post succesfully added!')
                return redirect("superuser_admin_page")
            else:
                messages.error(
                    request, "There was an error with your form.",
                )
                return redirect("superuser_admin_page")

    else:
        messages.warning(request, "You are not allowed to visit this page.")
        return redirect("shop")


@login_required
def manage_post(request, post_pk):
    """View for superuser management of blog posts"""

    if request.user.is_superuser:
        post = get_object_or_404(BlogPost, pk=post_pk)
        if request.method == "GET":
            form = BlogPostForm(instance=post)

            context = {
                'post': post,
                'form': form,
            }

            return render(request, 'superuser_admin/manage_post.html', context)
        else:
            blog_post_form = BlogPostForm(request.POST, instance=post)
            if blog_post_form.is_valid():
                blog_post_form.save()
                messages.success(request, 'Succesfully edited Post!')

                return redirect("superuser_admin_page")

    else:
        messages.warning(request, "You are not allowed to visit this page")
        return redirect("shop")


@login_required
def delete_post(request, post_pk):
    """View for the superuser to delete a blog post"""

    if request.user.is_superuser:
        post = get_object_or_404(BlogPost, pk=post_pk)
        post.delete()

        return redirect('superuser_admin_page')
    else:
        messages.warning(request, "You are not allowed to visit this page")
        return redirect("shop")


def superuser_view_product(request, sku):
    """
    View for the superuser to view products with ease from the admin panel
    """

    template = "shop/product_detail.html"

    product = get_object_or_404(Product, sku=sku)

    context = {
        "product": product,
        "from_superuser": True,
    }

    return render(request, template, context)
