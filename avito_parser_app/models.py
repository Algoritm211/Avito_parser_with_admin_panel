from django.db import models
import datetime

# Create your models here.

class Product(models.Model):
    title = models.TextField(
        verbose_name='Заголовок',
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена',
    )
    currency = models.TextField(
        verbose_name='Валюта',
        default='₽',
        null=True,
        blank=True
    )
    url = models.URLField(
        verbose_name='Cсылка на объявление',
        unique=True,
    )
    published_date = models.DateTimeField(
        verbose_name = 'Дата публикации',
        default=datetime.datetime.now(),
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'