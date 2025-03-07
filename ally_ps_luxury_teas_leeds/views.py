from django.shortcuts import render

"""Views to handle 404 and 500 errors"""


def handler404(request, exception):
    """Error Handler 404 - Page Not Found"""
    return render(request, "errors/404.html", status=404)


def handler500(request):
    """Error Handler 500 - Internal Server Error"""
    return render(request, "errors/500.html", status=500)
