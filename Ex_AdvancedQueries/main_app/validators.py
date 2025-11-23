from decimal import Decimal

from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError


@deconstructible
class RangeValidator:
    def __init__(self, min_value: Decimal | int, max_value: Decimal | int, message: str) -> None:
        self.min_value = min_value
        self.max_value = max_value
        self.message = message

    def __call__(self, value: Decimal) -> None:
        if not (self.min_value <= value <= self.max_value):
            raise ValidationError(self.message)

