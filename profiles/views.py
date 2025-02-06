from django.shortcuts import HttpResponse


def profile(request):
    """ Profile view """

    return HttpResponse("Hello does this work")
