from django.shortcuts import render

from .forms import EnquiryForm


def about(request):
    """View that renders the about page"""

    form = EnquiryForm

    context = {
        'form': form,
    }

    return render(request, 'about/about.html', context)
