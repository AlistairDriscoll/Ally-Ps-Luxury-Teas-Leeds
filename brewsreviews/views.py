from django.shortcuts import render
from .models import BlogPost


def main_blog_page(request):
    """View to generate the main blog page"""

    blog_posts = BlogPost.objects.all()

    context = {
        'blog_posts': blog_posts,
    }

    return render(request, 'blog/main_blog_page.html', context)
