from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Meta:
        db_table = 'user'
    def _str__(self):
        return self.username

class Subscriptions(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    subscribed_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribers')
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='subscriptions'
        unique_together=('subscriber','subscribed_to')
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(subscriber=models.F('subscribed_to')),
                name='cannot_subscribe_to_self'
            )
        ]
    
    def __str__(self):
        return f"{self.subscriber} → {self.subscribed_to}"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'tags'

    def __str__(self):
        return self.name

class Pulse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pulses')
    title = models.CharField(max_length=300)
    content = models.TextField()
    views = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(Tag, through='PulseTag', related_name='pulses')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'pulses'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class PulseTag(models.Model):
    pulse = models.ForeignKey(Pulse, on_delete=models.CASCADE)
    tag   = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pulse_tags'
        unique_together = ('pulse', 'tag')

class Reply(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    pulse       = models.ForeignKey(Pulse, on_delete=models.CASCADE, related_name='replies')
    content     = models.TextField()
    is_accepted = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'replies'
        ordering = ['-is_accepted', 'created_at']

    def __str__(self):
        return f"Reply by {self.user} on {self.pulse}"

class Comment(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    pulse      = models.ForeignKey(Pulse, on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
    reply      = models.ForeignKey(Reply, on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comments'
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(pulse__isnull=False, reply__isnull=True) |
                    models.Q(pulse__isnull=True,  reply__isnull=False)
                ),
                name='comment_must_belong_to_pulse_or_reply'
            )
        ]

    def __str__(self):
        target = f"pulse {self.pulse_id}" if self.pulse_id else f"reply {self.reply_id}"
        return f"Comment by {self.user} on {target}"


class Vote(models.Model):
    UP   = 1
    DOWN = -1
    VOTE_CHOICES = [(UP, 'Upvote'), (DOWN, 'Downvote')]

    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    pulse      = models.ForeignKey(Pulse, on_delete=models.CASCADE, null=True, blank=True, related_name='votes')
    reply      = models.ForeignKey(Reply, on_delete=models.CASCADE, null=True, blank=True, related_name='votes')
    value      = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'votes'
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(pulse__isnull=False, reply__isnull=True) |
                    models.Q(pulse__isnull=True,  reply__isnull=False)
                ),
                name='vote_must_target_pulse_or_reply'
            ),
            models.UniqueConstraint(fields=['user', 'pulse'],  condition=models.Q(pulse__isnull=False),  name='one_vote_per_pulse'),
            models.UniqueConstraint(fields=['user', 'reply'],  condition=models.Q(reply__isnull=False),  name='one_vote_per_reply'),
        ]

    def __str__(self):
        return f"{'Up' if self.value == 1 else 'Down'}vote by {self.user}"