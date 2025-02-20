from django.contrib import admin

from .models import Order, OrderItem


class OrderItemAdminInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ("item_total",)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAdminInline,)

    readonly_fields = (
        "order_number",
        "date",
        "delivery_cost",
        "order_total",
        "grand_total",
        "original_bag",
    )

    fields = (
        'order_number',
        'user_profile',
        'full_name',
        'email',
        'phone_number',
        'address_line1',
        'address_line2',
        'town_or_city',
        'state_or_region',
        'country',
        'postcode',
        'date',
        'delivery_cost',
        'order_total',
        'grand_total',
        'original_bag',
        'stripe_pid',
    )

    fields = (
        "order_number",
        "user_profile",
        "full_name",
        "email",
        "phone_number",
        "country",
        "postcode",
        "town_or_city",
        "address_line1",
        "address_line2",
        "state_or_region",
        "date",
        "delivery_cost",
        "order_total",
        "grand_total",
        "original_bag",
    )

    list_display = (
        "order_number",
        "date",
        "full_name",
        "order_total",
        "delivery_cost",
        "grand_total",
    )

    ordering = ("-date",)


admin.site.register(Order, OrderAdmin)
