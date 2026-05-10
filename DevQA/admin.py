from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Subscriptions, Tag, Pulse, PulseTag, Reply, Comment, Vote

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Subscriptions)
admin.site.register(Tag)
admin.site.register(Pulse)
admin.site.register(PulseTag)
admin.site.register(Reply)
admin.site.register(Comment)
admin.site.register(Vote)
