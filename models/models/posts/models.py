from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from models.models.users.models import User
from models.models.basics.models import Base


class Post(Base):
    PEN = 'PENDING'
    APP = 'APPROVED'
    REJ = 'REJECTED'

    STATUS_CHOICES = (
        (PEN, 'На модерации'),
        (APP, 'Одобрена'),
        (REJ, 'Отклонена'),
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
        upload_to='images/photos/originals/',
        blank=True,
        verbose_name='Изображение',
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(100, 100)],
        format='PNG',
        options={'quality': 60}
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default=PEN,
        verbose_name='Статус',
    )
   
    class Meta:
        db_table = 'posts'
        ordering = ['-created']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self) -> str:
        return self.title
    
    def get_votes_count(self) -> int:
        return self.votes.count()
