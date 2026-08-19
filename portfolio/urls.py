# App-level URL configuration for the "portfolio" app.
# Each path() below connects a URL to a view function in views.py,
# and gives it a "name" so templates can link to it with {% url %}
# instead of hardcoding the address.

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
]
