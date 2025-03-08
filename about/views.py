from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import EnquiryForm


def about(request):
    """View that renders the about page"""

    if request.method == "GET":
        form = EnquiryForm

        context = {
            'form': form,
        }

        return render(request, 'about/about.html', context)

    else:
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Thanks for getting in touch! I will reply soon.'
            )
            return redirect('about_us')
