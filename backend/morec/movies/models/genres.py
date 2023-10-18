from django.contrib.auth import get_user_model
from django.db import models

from .abstracts import SlugTitleAbstract
from .mixins import ImageDeleteMixin

User = get_user_model()


class Genre(SlugTitleAbstract, ImageDeleteMixin):
    image_fields = ('picture',)

    favorite = models.ManyToManyField(
        User,
        verbose_name='В избранном',
        related_name='fav_genres',
        blank=True,
    )
    picture = models.ImageField(
        verbose_name='Картинка',
        upload_to='images/genres/',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        db_table = 'genres'

    def delete(self, *args, **kwargs):
        self.picture.delete(save=False)
        return super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.remove_image_on_update()
        return super().save(*args, **kwargs)
