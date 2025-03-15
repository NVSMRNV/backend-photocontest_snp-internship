from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from api.services.notifications.notify import NotifyService
from models.models.basics.models import Base
from models.models.posts.models import Post
from models.models.users.models import User


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

    def __str__(self) -> str:
        return f'{self.user.username} проголосовал за {self.post.title}'
    
    class Meta:
        db_table = 'votes'
        unique_together = ('user', 'post')
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоса'
    

@receiver(post_save, sender=Vote)
def notify_new_vote(sender, instance, **kwargs):
    NotifyService.send(
        user_id=instance.post.author.id,
        message={
            'from_user': instance.user.username,
            'from_post_id': instance.post.id,
            'from_post_title': instance.post.title,
            'text': (
                f'{instance.user.username} проголосовал'
                f'за ваш пост {instance.post.title}!',
            )
        }
    )


@receiver(post_delete, sender=Vote)
def notify_deleted_vote(sender, instance, **kwargs):
    NotifyService.send(
        user_id=instance.post.author.id,
        message={
            'from_user': instance.user.username,
            'from_post_id': instance.post.id,
            'from_post_title': instance.post.title,
            'text': (
                f'{instance.user.username} удалил свой голос'
                f'c вашего проста {instance.post.title}!',
            )
        }
    )
