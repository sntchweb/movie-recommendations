import os

MIN_RATE = 1
MAX_RATE = 10

SHORT_DESCRIPT_LEN = 150

SITE_NAME = os.environ.get('SITE_NAME', 'http://localhost')

JWT_REGISTRATION_TTL = 3600  # время жизни токена для регистрации в секундах (1 час)
JWT_ACCESS_TTL = 3600 * 24 * 7  # время жизни access токена в секундах (неделя)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 2525
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

SOCIAL_AUTH_YANDEX_OAUTH2_KEY = os.environ.get('SOCIAL_AUTH_YANDEX_OAUTH2_KEY')
SOCIAL_AUTH_YANDEX_OAUTH2_SECRET = os.environ.get('SOCIAL_AUTH_YANDEX_OAUTH2_SECRET')
