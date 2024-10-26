import re

from user.constants import USERNAME_REGEX
from user.exceptions import UserValidationException

from email_validator import validate_email, EmailNotValidError


def validate_user_email(email: str):
    try:
        emailinfo = validate_email(email, check_deliverability=False)
        return emailinfo.normalized
    except EmailNotValidError as e:
        raise UserValidationException(str(e))


def validate_username(username: str):
    if not re.match(USERNAME_REGEX, username):
        raise UserValidationException("Только буквы, цифры и @/./+/-/_ разрешены.")
    return username
