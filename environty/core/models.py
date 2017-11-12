import re
import uuid

from django.core import exceptions
from django.db.models import fields
from django.db import models

from environty.core.utils.slug import SLUGID_NICE_REGEX, slug_to_uuid, slugid_nice, uuid_to_slug


class SlugField(fields.UUIDField):
    """ A UUID field with integrated slugid

    Subclassed from the standard UUIDField to convert between UUIDs and slugs.
    """
    def get_db_prep_value(self, value, connection, prepared=False):
        """ Prepares data for storage in the database

        Here, we convert the slug into a native UUID if the db (like postgres) supports;
        otherwise return the hex value for storing in a database varchar.
        """
        if value is None:
            return None
        if not isinstance(value, uuid.UUID):
            value = slug_to_uuid(value)
        if connection.features.has_native_uuid_field:
            return value
        return value.hex

    def from_db_value(self, value, expression, connection, context):
        """ Runs on every retrieval of data; converts our UUID to a slugid!
        """
        if value is None:
            return value
        return uuid_to_slug(value)

    def to_python(self, value):
        """ Converts the input value into the expected Python data type, in our case UUID
        """
        if isinstance(value, uuid.UUID) or value is None:
            return value
        if re.match(SLUGID_NICE_REGEX, value):
            return slug_to_uuid(value)
        else:
            raise exceptions.ValidationError('Could not convert {} to uuid'.format(value))


class SlugModel(models.Model):
    """ Model with a uuid4 slug

    Intended for models that will be looked up by some means in an API or URL.
    The slug is stored on the model as a uuid4, which is shortened for presentation and
    retrieval using the slugid library. Use slug for lookups instead of primary key.
    """
    slug = SlugField(default=slugid_nice, editable=False, db_index=True)

    class Meta:
        abstract = True
