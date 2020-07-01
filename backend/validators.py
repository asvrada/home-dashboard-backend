from django.core.exceptions import ValidationError

MIN_RANGE_NUMBER = -999999999
MAX_RANGE_NUMBER = 999999999


def make_validate_number_range(range_min=None, range_max=None):
    def validate_number_range(number):
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
                raise ValidationError(f"{number} not within range: {range_min} to {range_max} (inclusive)")

    return lambda value: validate_number_range(value)


def validate_enum(category, company, card):
    if category is not None and category.category != "CAT":
        raise ValidationError(
            {"category": f"Field category should have a enum of type category, got {category}"})

    if company is not None and company.category != "COM":
        raise ValidationError(
            {"company": f"Field company should have a enum of type company, got {company}"})

    if card is not None and card.category != "CAR":
        raise ValidationError(
            {"card": f"Field card should have a enum of type card, got {card}"})
