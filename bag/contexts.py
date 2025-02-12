def bag_contents(request):
    """
    For storing bag contents
    The context works the same as in views but is available in all apps as it
    is registered in settings
    """

    bag_items = 0

    context = {
        "bag_items": bag_items,
    }

    return context
