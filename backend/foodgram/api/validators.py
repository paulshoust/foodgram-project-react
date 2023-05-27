from rest_framework.exceptions import ValidationError


def positive_value_validator(value):
    """Validate fields that need to be positive."""
    if value <= 0:
        raise ValidationError('The value should be positive.')
