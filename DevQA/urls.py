from django.urls import path
from .views import (
    PulseListView,
    PulseDetailView,
    PulseCreateView
)
from . import views

urlpatterns = [
    path('',PulseListView.as_view(), name='devpulse-home'),
    path('pulse/<int:pk>/', PulseDetailView.as_view(), name='devpulse-detail'),
    path('pulse/new/', PulseCreateView.as_view(), name='devpulse-create'),
    path('about/',views.about, name='devpulse-about'),
]
