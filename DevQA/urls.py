from django.urls import path
from .views import (
    PulseListView,
    PulseDetailView,
    PulseCreateView,
    PulseUpdateView,
    PulseDeleteView
)
from . import views

urlpatterns = [
    path('',PulseListView.as_view(), name='devpulse-home'),
    path('pulse/<int:pk>/', PulseDetailView.as_view(), name='devpulse-detail'),
    path('pulse/new/', PulseCreateView.as_view(), name='devpulse-create'),
    path('pulse/<int:pk>/update/', PulseUpdateView.as_view(), name='devpulse-update'),
    path('pulse/<int:pk>/delete/', PulseDeleteView.as_view(), name='devpulse-delete'),
    path('about/',views.about, name='devpulse-about'),
]
