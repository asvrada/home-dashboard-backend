from django.core.exceptions import ValidationError

MIN_RANGE_NUMBER = -999999999
MAX_RANGE_NUMBER = 999999999


def validate_number_range(number, error_key: str, range_min=None, range_max=None):
    # Don't do validation
    if range_min is None and range_max is None:
        return

    if range_min is None:
        if number > range_max:
            raise ValidationError(f"{number} exceed maximum: {range_max}")

    if range_max is None:
        if number < range_min:
            raise ValidationError(f"{number} below minimum: {range_min}")

    # both min max is not None
    if range_min is not None and range_max is not None:
        if not range_min <= number <= range_max:
            raise ValidationError({
                error_key: f"{number} not within range: {range_min} to {range_max} (inclusive)"
            })


def validate_enum_category(enum, error_key: str, expected_category: str):
    if enum is None:
        return

    if enum is not None and enum.category != expected_category:
        raise ValidationError({
            error_key: f"Field EnumCategory should have a enum of type {expected_category}, got {enum}"
        })
