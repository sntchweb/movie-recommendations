from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .docs import urlpatterns as docs_urlpatterns
from .views.actors import ActorViewSet
from .views.analytics import get_movie_recommendations
from .views.categories import CategoryViewSet
from .views.compilations import (CompilationSoloViewSet,
                                 CompilationFavoriteListViewSet,
                                 CompilationRedactionListViewSet)
from .views.countries import CountryViewSet
from .views.directors import DirectorViewSet
from .views.genres import GenreViewSet
from .views.movies import MoviesViewSet
from .views.users import (AvatarViewSet, UsersMe, favorite_genres, login,
                          password_recovery, update_password,
                          user_create_activate, user_registration,
                          user_verify_email)

v1_router = DefaultRouter()
v1_router.register('avatars', AvatarViewSet)
v1_router.register('movies', MoviesViewSet)
v1_router.register('categories', CategoryViewSet)
v1_router.register('genres', GenreViewSet)
v1_router.register('countries', CountryViewSet)
v1_router.register(
    'compilations/redaction',
    CompilationRedactionListViewSet,
    basename="comp-redac"
)
v1_router.register(
    'compilations/favorite',
    CompilationFavoriteListViewSet,
    basename="comp-favorite"
)
v1_router.register('actors', ActorViewSet)
v1_router.register('directors', DirectorViewSet)

urlpatterns = [
    path('v1/auth/verify-email/', user_verify_email),
    path('v1/auth/user-registration/', user_registration),
    path('v1/auth/activation/<token>/', user_create_activate),
    path('v1/auth/login/', login),
    path('v1/auth/password-recovery/', password_recovery),
    path('v1/auth/reset-password/', update_password),
    path('v1/users-me/', UsersMe.as_view()),
    path('v1/users/favorite-genres/', favorite_genres),
    path('v1/users/special-for-you/', get_movie_recommendations),
    path('docs/', include(docs_urlpatterns)),
    path('v1/', include(v1_router.urls)),

    path(
        'v1/compilations/<int:pk>/',
        CompilationSoloViewSet.as_view(),
        name="compilation"
    ),
]
