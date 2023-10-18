from .abstracts import SlugTitleAbstract


class Category(SlugTitleAbstract):

    class Meta(SlugTitleAbstract.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'categories'
