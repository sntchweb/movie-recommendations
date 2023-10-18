from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from api.serializers.categories import CategorySerializer
from movies.models import Category


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description='Выдача списка категорий',
    tags=['Категории'],
))
class CategoryViewSet(ListModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
