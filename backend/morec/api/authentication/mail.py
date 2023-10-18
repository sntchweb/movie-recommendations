import datetime

import jwt
from rest_framework import status
from rest_framework.response import Response

from morec.settings import (EMAIL_HOST_USER, JWT_REGISTRATION_TTL, SECRET_KEY,
                            SITE_NAME)

from ..tasks import send_email


def sending_mail(email):
    payload = {"exp": datetime.datetime.now(
        tz=datetime.timezone.utc) + datetime.timedelta(
        JWT_REGISTRATION_TTL), "email": email}
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    subject = 'Восстановление пароля КиноТочка'
    message = (
        f'Для восстановления пароля перейдите по ссылке\n '
        f'{SITE_NAME}/reset-password/{encoded_jwt}/\n'
        f'ссылка активна 1 час'
    )
    recipient = email
    send_email.delay(subject, message, [recipient], EMAIL_HOST_USER)
    return Response(status=status.HTTP_200_OK)
