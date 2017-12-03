import re
import uuid

from django.core import exceptions
import slugid


SLUGID_V4_REGEX = re.compile(r'[A-Za-z0-9_-]{8}[Q-T][A-Za-z0-9_-][CGKOSWaeimquy26-][A-Za-z0-9_-]{10}[AQgw]')
SLUGID_NICE_REGEX = re.compile(r'[A-Za-f][A-Za-z0-9_-]{7}[Q-T][A-Za-z0-9_-][CGKOSWaeimquy26-][A-Za-z0-9_-]{10}[AQgw]')


def slugid_nice():
    """ Returns a new, random utf-8 slug (based on uuid4).

    :return: slug representation of a new uuid4, as a utf-8 string
    :rtype: str
    """
    return slugid.nice().decode('utf-8')


def slug_to_uuid(slug):
    """ Returns a uuid.UUID object from a slug.

    :param str slug: slug to convert to UUID
    :return: uuid representation of slug
    :rtype: uuid.UUID
    """
    try:
        uuid_out = slugid.decode(slug)
    except Exception as ex:
        raise exceptions.ValidationError('slug could not be decoded')
    return uuid_out


def uuid_to_slug(uuid_in):
    """ Returns a utf-8 slug representation of a UUID.

    :param uuid.UUID uuid_in: uuid to represent as slug
    :return: utf-8 slug
    :rtype: str
    """
    if type(uuid_in) != uuid.UUID:
        try:
            uuid_in = uuid.UUID(uuid_in)
        except (AttributeError, ValueError):
            raise exceptions.ValidationError('invalid uuid value')
    return slugid.encode(uuid_in).decode('utf-8')
