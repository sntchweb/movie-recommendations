from .abstracts import PersonAbstract


class Actor(PersonAbstract):

    class Meta(PersonAbstract.Meta):
        verbose_name = 'Актёр'
        verbose_name_plural = 'Актёры'
        default_related_name = 'fav_actors'
        db_table = 'actors'
