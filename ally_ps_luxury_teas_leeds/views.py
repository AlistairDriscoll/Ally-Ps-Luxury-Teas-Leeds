from django.shortcuts import render


def about_us(request):
    """Renders the about us page"""

    return render(request, 'about_us.html')
