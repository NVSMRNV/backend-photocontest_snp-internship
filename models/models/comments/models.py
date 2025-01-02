from django.db import models

from models.models.users.models import User
from models.models.posts.models import Post
from models.models.basics.models import Base


class Comment(Base):
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    post = models.ForeignKey(
        'Post',
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

