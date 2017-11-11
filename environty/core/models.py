import uuid

from django.utils.functional import cached_property
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import slugid


def _replace_slug(anydict):
    """ Replace slug in anydict with decoded uuid

    :param dict anydict: a dictionary that might have a key named 'slug'
    :return: a dictionary where slug is replaced by the decoded uuid
    """
    if 'slug' in anydict.keys():
        try:
            anydict['uuid'] = slugid.decode(anydict['slug'])
        except ValueError as ex:
            raise ObjectDoesNotExist('could not match slug {} to any know object ({})'.format(anydict['slug'], ex))
        anydict.pop('slug')
    return anydict


class SlugModelManager(models.Manager):
    """ Manager for SlugModels
    Allows get and filter lookups in the form of MyModel.objects.get(slug='fF_O8LITQECXPy1BsALZMQ')
    """
    def get(self, **kwargs):
        kwargs = _replace_slug(kwargs)
        return super(SlugModelManager, self).get(**kwargs)

    def filter(self, **kwargs):
        kwargs = _replace_slug(kwargs)
        return super(SlugModelManager, self).filter(**kwargs)


class SlugModel(models.Model):
    """ Model with a uuid4 slug

    Intended for models that will be looked up by some means in an API or URL.
    The slug is stored on the model as a uuid4, which is shortened for presentation and
    retrieval using the slugid library. Use slug for lookups instead of primary key.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    objects = SlugModelManager()

    class Meta:
        abstract = True
        default_manager_name = 'objects'

    @cached_property
    def slug(self):
        return slugid.encode(self.uuid).decode('utf-8')