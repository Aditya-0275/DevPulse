from django.shortcuts import render
from django.http import HttpResponse
from .models import Pulse

def home(request):
    context = {
        'pulses': Pulse.objects.all()
    }
    return render(request, 'DevQA/home.html', context=context)

def about(request):
    return render(request, 'DevQA/about.html', {'title': 'About DevPulse'})
    
