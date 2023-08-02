import abc
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from apps.account.models import Account


class BaseAuthBackend(abc.ABC):
    @abc.abstractmethod
    def authenticate(self, request: WSGIRequest,
                     **credentials) -> User | None: ...

    @abc.abstractmethod
    def get_user(self, user_id: int) -> User | None: ...


class EmailAuthBackend(BaseAuthBackend):
    def authenticate(self, request: WSGIRequest, **credentials) -> User | None:
        if (email := credentials.get('username')) is None:
            return None
        if password := credentials.get('password1') is None:
            return None

        try:
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


def create_account(backend, user, *args, **kwargs):
    Account.objects.get_or_create(user=user)
