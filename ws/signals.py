import json

from django.db.models.signals import post_save
from django.dispatch import receiver

from models.models.votes.models import Vote
from models.models.comments.models import Comment

from ws.utils import send_ws_notification
from asgiref.sync import sync_to_async


@receiver(post_save, sender=Vote)
def notify_vote(sender, instance, created, **kwargs):
    if created:
        message = {
            "type": "vote",
            "post_id": instance.post.id,
            "post_title": instance.post.title,
            "user": instance.user.username,
            "text": f"{instance.user.username} проголосовал за ваш пост!",
        }
        send_ws_notification(instance.post.author.id, message)
