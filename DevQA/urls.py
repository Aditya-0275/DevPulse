from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='devpulse-home'),
    path('about/',views.about, name='devpulse-about'),
]