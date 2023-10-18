from datetime import datetime

from django.contrib import admin
from import_export import fields, resources, widgets
from import_export.admin import ImportExportModelAdmin

from movies.models import Genre
from users.forms import AvatarForm
from users.models import Avatar, User


class UserResource(resources.ModelResource):
    fav_genres = fields.Field(
        attribute='fav_genres',
        column_name='fav_genres',
        widget=widgets.ManyToManyWidget(Genre, field='title', separator=' '),
    )
    fav_genres_id = fields.Field(
        attribute='fav_genres',
        column_name='fav_genres',
        widget=widgets.ManyToManyWidget(Genre, field='id', separator=' '),
    )

    class Meta:
        fields = ('id', 'sex', 'date_of_birth', 'fav_genres', 'fav_genres_id')
        export_order = (
            'id', 'sex', 'date_of_birth', 'fav_genres', 'fav_genres_id'
        )
        model = User

    def dehydrate_date_of_birth(self, obj):
        if obj.date_of_birth is None:
            return 0
        today = datetime.today()
        age = today.year - obj.date_of_birth.year
        if (today.month < obj.date_of_birth.month) or (
                today.month == obj.date_of_birth.month and
                today.day < obj.date_of_birth.day):
            age -= 1
        return age

    def dehydrate_sex(self, obj):
        return 'Male' if obj.sex == 0 else 'Female' if obj.sex == 1 else ''


class UserFavGenre(admin.TabularInline):
    model = Genre.favorite.through


class UserAdmin(ImportExportModelAdmin):
    resource_classes = (UserResource, )
    list_display = ('email', )
    list_filter = ('email', )
    inlines = [UserFavGenre, ]


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    form = AvatarForm


admin.site.register(User, UserAdmin)
