from django.conf import settings
from django.db import models


class Ad(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название товара', help_text='Введите название товара')
    price = models.PositiveIntegerField(verbose_name='Цена товара', help_text='Введите название товара')
    description = models.CharField(max_length=1000, verbose_name='Описание товара',
                                   help_text='Опишите товар', null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='ads',
                               verbose_name='Автор объявления')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания объявления')
    image = models.ImageField(upload_to='pictures/ad/', null=True, blank=True,
                              verbose_name='Обложка объявления')

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]


class Comment(models.Model):
    text = models.CharField(max_length=1000, verbose_name='Комментарий', help_text='Вы можете оставить комментарий')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments",
                               verbose_name="Автор комментария")
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="comments_ad",
                           verbose_name="Объявление, к которому относится комментарий")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания комментария', null=True)
