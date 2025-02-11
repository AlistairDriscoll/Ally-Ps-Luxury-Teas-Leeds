from django.shortcuts import render


def view_bag(request):
    """View to view the contents of the basket in full"""
    return render(request, "bag/bag.html")


def add_to_bag(request):
    """View to add products to the basket"""
