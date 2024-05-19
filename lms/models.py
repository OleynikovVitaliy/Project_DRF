from django.conf import settings
from django.db import models

from config.settings import AUTH_USER_MODEL

NULLABLE = {'blank': True, 'null': True}


class Well(models.Model):
    """
    Модель Курса
    """
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='preview/', verbose_name='Изображение', **NULLABLE)
    video_link = models.CharField(max_length=300, verbose_name='Ссылка на видео', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, default="", on_delete=models.CASCADE,
                              **NULLABLE, verbose_name="Владелец")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    """
    Модель Урока
    """
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='preview/', verbose_name='Изображение', **NULLABLE)
    well = models.ForeignKey('Well', on_delete=models.CASCADE, verbose_name='Курс', **NULLABLE)
    video_link = models.CharField(max_length=300, verbose_name='Ссылка на видео', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, default="", on_delete=models.CASCADE,
                              **NULLABLE, verbose_name="Владелец")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Subscription(models.Model):
    """
    Модель подписки
    """
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Пользователь')
    well = models.ForeignKey('Well', on_delete=models.CASCADE, verbose_name='Курс')
    is_active = models.BooleanField(default=False, verbose_name='Активна')

    def __str__(self):
        return f'Подписка на курс {self.well}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
