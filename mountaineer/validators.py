from decimal import Decimal
from uuid import UUID
from strainer import validators, ValidationException


@validators.export_validator
def enum_validator(value, context=None, enum=None):
    try:
        if value in enum.__members__.keys():
            return value
        else:
            raise ValidationException('invalid enum value: {}'.format(value))
    except:
        raise ValidationException('invalid enum value: {}'.format(value))


@validators.export_validator
def is_decimal(value, context=None):
    if type(value) == Decimal:
        return value
    try:
        as_decimal = Decimal(value)
        return as_decimal
    except:
        raise ValidationException('{} cannot be expressed as a decimal'.format(value))


@validators.export_validator
def is_uuid(value, context=None):
    if value:
        try:
            UUID(value)
        except:
            raise ValidationException('{} is not a UUID'.format(value))
    return value
