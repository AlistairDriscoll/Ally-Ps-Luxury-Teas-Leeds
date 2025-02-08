from django.shortcuts import render


def index(request):
    """
    View to return to the index page
    """

    return render(request, 'welcome/index.html')
