from django.shortcuts import render


def about(request):
    """View that renders the about page"""

    return render(request, 'about/about.html')
