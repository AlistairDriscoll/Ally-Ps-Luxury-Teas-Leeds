from django.shortcuts import render, get_object_or_404
from .models import BlogPost


def main_blog_page(request):
    """View to generate the main blog page"""

    blog_posts = BlogPost.objects.all()

    context = {
        'blog_posts': blog_posts,
    }

    return render(request, 'brewsreviews/main_blog_page.html', context)


def blog_post(request, pk):
    """View to render the page of a full blog post"""

    post = get_object_or_404(BlogPost, pk=pk)

    context = {
        'post': post,
    }

    return render(request, 'brewsreviews/blog_post.html', context)
