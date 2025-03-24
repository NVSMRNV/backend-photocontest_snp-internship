from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.services.notifications.notify import NotifyService
from models.models.basics.models import Base
from models.models.users.models import User


class Comment(Base):
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    post = models.ForeignKey(
        'models.Post',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост',
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name='Родительский комментарий',
        null=True,
        blank=True,
    )
    text = models.TextField(
        verbose_name='Текс',
        max_length=512,
    )

    class Meta:
        db_table = 'comments'
        ordering = ['-created']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text


@receiver(post_save, sender=Comment)
def notify_new_comment(sender, instance, **kwargs):
    NotifyService.send(
        user_id=instance.post.author.id, 
        message={
            'text': (
                f'Под вашим постом "{instance.post.title}"'
                f'{instance.author} оставил комментарий!'
            )
        }
    )
