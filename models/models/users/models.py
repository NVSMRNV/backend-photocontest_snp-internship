from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, pre_save
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from models.models.basics.models import Base
from utils.file_uploader import save_file, skip_saving_file, uploaded_file_path


class User(AbstractUser, Base):
    username = models.CharField(
        verbose_name='Имя',
        max_length=128,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Почта',
        blank=True,
    )
    bio = models.TextField(
        verbose_name='Информация',
        blank=True,
    )
    profile_photo = models.ImageField(
        verbose_name='Фото профиля',
        upload_to=uploaded_file_path,
        default='static/images/users/default.png',
        blank=True,
    )
    profile_photo_thumbnail = ImageSpecField(
        source='profile_photo',
        processors=[ResizeToFill(100, 100)],
        format='PNG',
        options={'quality': 60}
    )

    last_name = None
    first_name = None
    date_joined = None

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'users'
        ordering = ['-created']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


pre_save.connect(skip_saving_file, sender=User)
post_save.connect(save_file, sender=User)