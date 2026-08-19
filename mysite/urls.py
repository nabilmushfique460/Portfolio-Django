"""
Project-level URL configuration.

This file is the "front door" for every URL request that comes into
the Django project. It doesn't define any pages itself - instead it
hands off ("includes") all normal site traffic to the portfolio app's
own urls.py, and keeps the built-in Django admin site available at
/admin/.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django's built-in admin site (login required).
    path('admin/', admin.site.urls),

    # Every other URL ("", "about/", "services/", "contact/", ...) is
    # handled by portfolio/urls.py.
    path('', include('portfolio.urls')),
]
