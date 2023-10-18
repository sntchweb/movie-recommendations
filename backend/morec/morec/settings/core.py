import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

dotenv_file = BASE_DIR.joinpath('.env')

if dotenv_file.is_file():
    load_dotenv(dotenv_file)

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = True if os.environ.get('DEBUG') == 'True' else False

ALLOWED_HOSTS = ['*']

CORS_ALLOWED_ORIGINS = [
    'http://kinotochka.acceleratorpracticum.ru',
    'http://localhost:3000',
    'http://localhost:8000',
    'http://80.87.109.207',
    'http://80.87.109.242',
    'http://80.87.109.33',
    'http://80.87.109.84',
    'http://80.87.109.234',
    'http://bugaton1.acceleratorpracticum.ru',
    'http://bugaton2.acceleratorpracticum.ru',
    'http://bugaton3.acceleratorpracticum.ru',
    'http://bugaton4.acceleratorpracticum.ru',
    'http://bugaton5.acceleratorpracticum.ru',
]

CSRF_TRUSTED_ORIGINS = [
    'http://kinotochka.acceleratorpracticum.ru',
    'http://localhost:3000',
    'http://localhost:8000',
    'http://80.87.109.207',
    'http://80.87.109.242',
    'http://80.87.109.33',
    'http://80.87.109.84',
    'http://80.87.109.234',
    'http://bugaton1.acceleratorpracticum.ru',
    'http://bugaton2.acceleratorpracticum.ru',
    'http://bugaton3.acceleratorpracticum.ru',
    'http://bugaton4.acceleratorpracticum.ru',
    'http://bugaton5.acceleratorpracticum.ru',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'django_filters',
    'import_export',
    'social_django',
]

PROJECT_APPS = [
    'api',
    'users',
    'movies',
    # 'analytics',
]

INSTALLED_APPS += PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.yandex.YandexOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'morec.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'morec.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static-backend/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'
