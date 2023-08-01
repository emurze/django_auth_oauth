from django.core.exceptions import ValidationError


class EmailValidationError(ValidationError):
    message = 'Email must exists.'


class PasswordValidationError(ValidationError):
    message = 'Password must exists.'
