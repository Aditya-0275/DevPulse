from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse
from .models import Pulse


@login_required
def home(request):

    context = {
        'pulses': Pulse.objects.all()
    }
    return render(request, 'DevQA/home.html', context=context)

from django.db.models import Q

class PulseListView(ListView):
    model = Pulse
    template_name = 'DevQA/home.html'
    context_object_name = 'pulses'
    ordering = ['-created_at']

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            return qs.filter(Q(isPrivate=False) | Q(user=self.request.user))
        return qs.filter(isPrivate=False)

class PulseDetailView(DetailView):
    model = Pulse

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            return qs.filter(Q(isPrivate=False) | Q(user=self.request.user))
        return qs.filter(isPrivate=False)

class PulseCreateView(LoginRequiredMixin,CreateView):
    model = Pulse
    fields = ['title', 'content', 'isPrivate']
    template_name = 'DevQA/pulse_form.html'
    success_url = '/'


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PulseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Pulse
    fields = ['title', 'content', 'isPrivate']
    template_name = 'DevQA/pulse_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        pulse = self.get_object()
        if self.request.user == pulse.user:
            return True
        return False

class PulseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Pulse
    success_url = '/'
    template_name = 'DevQA/pulse_confirm_delete.html'

    def test_func(self):
        pulse = self.get_object()
        if self.request.user == pulse.user:
            return True
        return False

def about(request):
    return render(request, 'DevQA/about.html', {'title': 'About DevPulse'})
    
