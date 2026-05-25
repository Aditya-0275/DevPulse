from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView
)
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

class PulseCreateView(CreateView):
    model = Pulse
    fields = ['title', 'content', 'isPrivate']
    template_name = 'DevQA/pulse_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def about(request):
    return render(request, 'DevQA/about.html', {'title': 'About DevPulse'})
    
