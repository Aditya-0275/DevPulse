from django.shortcuts import render
from django.http import HttpResponse

discussion_thread = [
    {
        'author': 'Aditya Sharma',
        'title': 'First Post for DevPulse',
        'content': 'First Post Content.',
        'date_posted': 'May 04, 2026',
        'isPrivate': False
    },
    {
        'author': 'Mimansha',
        'title': 'Second Post for DevPulse',
        'content': 'Second Post Content.',
        'date_posted': 'May 04, 2026',
        'isPrivate': False
    },
    {
        'author': 'Aditya Sharma',
        'title': 'Third Post for DevPulse',
        'content': 'Third Post Content.',
        'date_posted': 'May 04, 2026',
        'isPrivate': True
    }
]

def home(request):
    context = {
        'discussion_thread': discussion_thread
    }
    return render(request, 'DevQA/home.html', context=context)

def about(request):
    return render(request, 'DevQA/about.html', {'title': 'About DevPulse'})
    
