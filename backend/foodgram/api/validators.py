from rest_framework.exceptions import ValidationError


def positive_value_validator(value):
    """Validate fields that need to be positive."""
    MINIMUM_VALUE = 0
    if value <= MINIMUM_VALUE:
        raise ValidationError('The value should be positive.')


def max_integer_field_validator(value):
    """Validate for IntegerFields and SmallIntegerFields."""
    MAXIMUM_INTEGERFIELD_VALUE = 32000
    if value > MAXIMUM_INTEGERFIELD_VALUE:
        raise ValidationError('The value shall not exceed 32 000')
