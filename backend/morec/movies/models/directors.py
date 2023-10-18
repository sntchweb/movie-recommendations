from .abstracts import PersonAbstract


class Director(PersonAbstract):

    class Meta(PersonAbstract.Meta):
        verbose_name = 'Режиссёр'
        verbose_name_plural = 'Режиссёры'
        default_related_name = 'fav_directors'
        db_table = 'directors'
