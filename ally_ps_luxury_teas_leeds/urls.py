from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500
from . import views

urlpatterns = [
    path("blog/", include("brewsreviews.urls")),
    path("about/", include("about.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("profile/", include("profiles.urls")),
    path("shop/", include("shop.urls")),
    path("bag/", include("bag.urls")),
    path("checkout/", include("checkout.urls")),
    path("", include("welcome.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

"""
    Handler urls and views made with the help of my menton Julias e_commerce
    app, ChatGPT and Code Institute walkthrough
"""
handler404 = views.handler404 # noqa
handler500 = views.handler500 # noqa
