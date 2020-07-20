from django.core.exceptions import ValidationError
import re


def validate_password(value: str):
    def exception(condition, description):
        if condition:
            raise ValidationError(description)

    exception(len(value) < 12, 'Password must be at least 12 characters')
    exception(not re.search(r'[0-9]+', value), 'Password must contain at least one number')
    exception(not re.search(r'\W|_', value), 'Password must contain at least one symbol')
    exception(not re.search(r'[a-zA-Z]', value), 'Password must contain at least one letter')
    exception(value.upper() == value or value.lower() == value, 'Password must contain letters of different cases')


def check_positive_numbers(value: int, name):
    if value < 0:
        raise ValidationError(f"{name} must be zero or positive")
