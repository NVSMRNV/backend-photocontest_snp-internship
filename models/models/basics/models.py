from django.db import models


class Base(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано',
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлено',
    )

    class Meta: 
        abstract = True
