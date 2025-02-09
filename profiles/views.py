from django.shortcuts import render


def profile(request):
    """ Profile view """

    return render(request, 'profiles/profile.html')
