from .abstracts import SlugTitleAbstract


class Country(SlugTitleAbstract):

    class Meta(SlugTitleAbstract.Meta):
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        db_table = 'countries'
