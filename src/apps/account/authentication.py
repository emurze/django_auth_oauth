import abc

from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest

from apps.account.exceptions import EmailValidationError, \
    PasswordValidationError


class BaseAuthBackend(abc.ABC):
    @abc.abstractmethod
    def authenticate(self, request: WSGIRequest,
                     **credentials) -> User | None: ...

    @abc.abstractmethod
    def get_user(self, user_id: int) -> User | None: ...


class EmailAuthBackend(BaseAuthBackend):
    def authenticate(self, request: WSGIRequest, **credentials) -> User | None:
        try:
            if (password := credentials.get('password')) is None:
                raise PasswordValidationError
            if (email := credentials.get('username')) is None:
                raise EmailValidationError

            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
            else:
                return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id: int) -> User | None:
        try:
            user = User.objects.get(id=user_id)
            return user
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None
