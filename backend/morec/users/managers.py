from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        """Создает и сохраняет пользователя с введенным им email и паролем."""
        if not email:
            raise ValueError('Пользователи должны иметь электронную почту')

        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Создает и сохраняет суперпользователя с указанным адресом электронной
        почты и паролем.
        """
        user = self.create_user(
            email,
            password=password
        )
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user
