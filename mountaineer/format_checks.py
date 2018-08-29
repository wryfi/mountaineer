"""
This module contains custom type formats for Connexion to use when validating
input data.

"""

from jsonschema import draft4_format_checker
from validators.email import email as valid_email
from validators.url import url as valid_url
from validators.uuid import uuid as valid_uuid


@draft4_format_checker.checks('uuid')
def validate_uuid(value):
    if valid_uuid(value):
        return True
    return False


@draft4_format_checker.checks('email')
def validate_email(value):
    if valid_email(value):
        return True
    return False


@draft4_format_checker.checks('url')
def validate_url(value):
    if valid_url(value):
        return True
    return False
