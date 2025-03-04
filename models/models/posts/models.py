from django.db import models
from django.dispatch import receiver
from django.db.models.signals import (
    post_save, 
    post_delete,
    pre_save, 
    pre_delete,
)


from django_fsm import FSMField, transition
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from models.models.users.models import User
from models.models.basics.models import Base
from api.services.notifications.notify import NotifyService

from utils.file_uploader import save_file, skip_saving_file, uploaded_file_path


class Post(Base):
    PEN = 'PENDING'
    APP = 'APPROVED'
    REJ = 'REJECTED'

    STATUS_CHOICES = (
        (PEN, 'На модерации'),
        (APP, 'Одобрен'),
        (REJ, 'Отклонен'),
    )
       
    author = models.ForeignKey(
        'User', 
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
    # status = models.CharField(
    #     max_length=20, 
    #     choices=STATUS_CHOICES,
    #     default=PEN,
    #     verbose_name='Статус',
    # )

    status = FSMField(
        default=PEN, 
        choices=STATUS_CHOICES, 
        protected=True,
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

    @transition(field=status, source='*', target=APP)
    def to_state_app(self):
        NotifyService.send(
            self.author.id,
            {'type': 'status_change', 'text': 'Ваш пост одобрен!'}
        )
        return 'Статус изменен на "Одобрен".'

    @transition(field=status, source=PEN, target=REJ)
    def to_state_rej(self):
        NotifyService.send(
            self.author.id,
            {'type': 'status_change', 'text': 'Ваш пост отклонен.'}
        )
        return 'Статус изменен на "Отклонен".'

    @transition(field=status, source='*', target=PEN)
    def to_state_pen(self):
        NotifyService.send(
            self.author.id, 
            {'type': 'status_change', 'text': 'Ваш пост снова на модерации.'}
        )
        return 'Статус изменен на "На модерации".'

    class Meta:
        db_table = 'posts'
        ordering = ['-created']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self) -> str:
        return self.title


pre_save.connect(skip_saving_file, sender=Post)
post_save.connect(save_file, sender=Post)


@receiver(pre_delete, sender=Post)
def notify_delete_post(sender, instance, **kwargs):
    comment_authors = (
        instance.comments.values_list('author_id', flat=True).distinct()
    )

    message = {
        'type': 'delete post',
        'text': 'Пост "{instance.title}" скоро будет удален.',
    }

    for author_id in comment_authors:
        NotifyService.send(author_id, message)



    
