from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from api.services.notifications.notify import NotifyService
from models.models.users.models import User
from models.models.posts.models import Post
from models.models.basics.models import Base


class Vote(Base):
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='votes',
        verbose_name='Пользователь',
    )
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='votes',
        verbose_name='Пост',
    )

    class Meta:
        db_table = 'votes'
        unique_together = ('user', 'post')
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоса'

    def __str__(self) -> str:
        return f'{self.user.username} проголосовал за {self.post.title}'


@receiver(post_save, sender=Vote)
def increase_votes_number(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        post.votes_number += 1
        post.save()


@receiver(post_delete, sender=Vote)
def decrease_votes_number(sender, instance, **kwargs):
    post = instance.post
    post.votes_number -= 1
    post.save()
    

@receiver(post_save, sender=Vote)
def notify_add_vote(sender, instance, **kwargs):
    message = {
        'type': 'add vote',
        'post_id': instance.post.id,
        'post_title': instance.post.title,
        'user': instance.user.username,
        'text': f'{instance.user.username} проголосовал за ваш пост!',
    }
    NotifyService.send(instance.post.author.id, message)


# @receiver(pre_delete, sender=Vote)
# def notify_delete_vote(sender, instance, **kwargs):
#     message = {
#         'type': 'delete vote',
#         'post_id': instance.post.id,
#         'post_title': instance.post.title,
#         'user': instance.user.username,
#         'text': f'{instance.user.username} удалил свой голос!',
#     }
#     NotifyService.send(instance.post.author.id, message)


@receiver(post_delete, sender=Vote)
def notify_delete_vote(sender, instance, **kwargs):
    message = {
        'type': 'delete vote',
        'post_id': instance.post.id,
        'post_title': instance.post.title,
        'user': instance.user.username,
        'text': f'{instance.user.username} удалил свой голос!',
    }
    NotifyService.send(instance.post.author.id, message)
