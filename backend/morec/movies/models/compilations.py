from django.contrib.auth import get_user_model
from django.db import models

from .mixins import ImageDeleteMixin

User = get_user_model()


class Compilation(models.Model, ImageDeleteMixin):
    image_fields = ('picture',)

    title = models.CharField(verbose_name='Название', max_length=100)
    description = models.TextField(verbose_name='Информация', blank=True)
    picture = models.ImageField(
        verbose_name='Фото',
        upload_to='images/compilations/',
    )
    movies = models.ManyToManyField(
        'Movie',
        verbose_name='Фильмы',
        related_name='compilations',
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='compilations'
    )
    favorite = models.ManyToManyField(
        User,
        verbose_name='Избранные подборки',
        related_name='favorite_compilations',
        blank=True,
    )
    from_redaction = models.BooleanField(
        verbose_name='От редакции',
        default=False,
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'
        db_table = 'compilations'

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.picture.delete(save=False)
        return super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.remove_image_on_update()
        return super().save(*args, **kwargs)
