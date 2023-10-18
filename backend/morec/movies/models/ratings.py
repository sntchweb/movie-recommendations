from django.db import models

from .abstracts import RatingAbstract


class RatingMovie(RatingAbstract):
    movie = models.ForeignKey(
        'Movie',
        verbose_name='Фильм',
        on_delete=models.CASCADE,
        related_name='ratings',
    )

    class Meta(RatingAbstract.Meta):
        verbose_name = 'Оценка фильма'
        verbose_name_plural = 'Оценки фильмов'
        default_related_name = 'movies_ratings'
        db_table = 'movies_ratings'


class RatingCompilation(RatingAbstract):
    compilation = models.ForeignKey(
        'Compilation',
        verbose_name='Подборка',
        on_delete=models.CASCADE,
        related_name='ratings',
    )

    class Meta(RatingAbstract.Meta):
        verbose_name = 'Оценка подборки'
        verbose_name_plural = 'Оценки подборок'
        default_related_name = 'compilations_ratings'
        db_table = 'compilations_ratings'
