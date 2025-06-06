from django.db import models
from django.db.models.signals import (
    post_delete, 
    post_save,
    pre_delete,
    pre_save
)
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from api.services.notifications.notify import NotifyService
from models.models.basics.models import Base
from models.models.comments.models import Comment
from models.models.votes.models import Vote
from utils.file_uploader import (
    save_file,
    skip_saving_file,
    uploaded_file_path,
)

class State(models.TextChoices):
    PEN = 'PENDING', _('Pending')
    APP = 'APPROVED', _('Approved')
    REJ = 'REJECTED', _('Rejected')
    DEL = 'ONDELETE', _('On delete')


class Post(Base):       
    author = models.ForeignKey(
        'models.User', 
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=128,
        verbose_name='Заголовок',
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    image = models.ImageField(
        upload_to=uploaded_file_path,
        verbose_name='Изображение',
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(100, 100)],
        format='PNG',
        options={'quality': 60}
    )
    state = models.CharField(
        max_length=50,
        default=State.PEN,
        choices=State.choices,
        verbose_name='Статус',
    )
    votes_number = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество голосов'
    )
    comments_number = models.PositiveBigIntegerField(
        default=0,
        verbose_name='Количество комментариев'
    )

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        db_table = 'posts'
        ordering = ['-created']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


pre_save.connect(skip_saving_file, sender=Post)
post_save.connect(save_file, sender=Post)


#! Голоса 
@receiver(post_save, sender=Vote)
def increase_votes_number(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        post.votes_number += 1
        post.save()


@receiver(post_delete, sender=Vote)
def decrease_votes_number(sender, instance, **kwargs):
    post = instance.post
    if post.votes_number > 0:
        post.votes_number -= 1
        post.save()


#! Комменты
@receiver(post_save, sender=Comment)
def increase_comments_number(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        post.comments_number += 1
        post.save()


@receiver(post_delete, sender=Comment)
def decrease_comments_number(sender, instance, **kwargs):
    post = instance.post
    if post.comments_number > 0:
        post.comments_number -= 1
        post.save()


#! Уведомления
@receiver(pre_delete, sender=Post)
def notify_delete_post(sender, instance, **kwargs):
    comment_authors = (
        instance.comments.values_list('author_id', flat=True).distinct()
    )

    for author_id in comment_authors:
        NotifyService.send(
            user_id=author_id, 
            message={
                'text': f'Пост "{instance.title}"скоро будет удален с Вашими комментариями.'
            }
        )
