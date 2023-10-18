from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from api.serializers.countries import CountrySerializer
from movies.models import Country


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description='Выдача списка стран',
    tags=['Страны'],
))
class CountryViewSet(ListModelMixin, GenericViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
