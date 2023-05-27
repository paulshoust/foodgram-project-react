from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

color_validator = RegexValidator(
    regex=r'^#[0-9A-Fa-f]{6}$',
    message='Неверно введен код цвета. Надо использовать HEX коды'
)
