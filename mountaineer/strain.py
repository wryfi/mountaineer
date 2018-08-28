"""
This module contains formatters and validators for data types
not defined in OpenAPI v2 (therefore not validated natively
by connexion) and not supported by strainer.
"""

from strainer import formatters, validators, ValidationException

from validators.email import email as valid_email
from validators.url import url as valid_url
from validators.uuid import uuid as valid_uuid


@formatters.export_formatter
def enum_formatter(value, context=None):
    return value.name


@validators.export_validator
def email_validator(value, context=None):
    if value:
        if valid_email(value):
            return value
        else:
            raise ValidationException('{} is not a valid email address'.format(value))
    return value


@validators.export_validator
def enum_validator(value, context=None, enum=None):
    if value:
        try:
            if value in enum.__members__.keys():
                return value
            else:
                raise ValidationException('invalid enum value: {}'.format(value))
        except:
            raise ValidationException('invalid enum value: {}'.format(value))
    return value


@validators.export_validator
def uuid_validator(value, context=None):
    if value:
        if valid_uuid(value):
            return value
        else:
            raise ValidationException('{} is not a UUID'.format(value))
    return value


@validators.export_validator
def url_validator(value, context=None):
    if value:
        if valid_url(value):
            return value
        else:
            raise ValidationException('{} is not a valid URL'.format(value))
    return value
