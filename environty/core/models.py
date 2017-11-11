import uuid

from django.utils.functional import cached_property
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import slugid


def _replace_slug(anydict):
    if 'slug' in anydict.keys():
        try:
            anydict['uuid'] = slugid.decode(anydict['slug'])
        except ValueError as ex:
            raise ObjectDoesNotExist('could not match slug {} to any know object ({})'.format(anydict['slug'], ex))
        anydict.pop('slug')
    return anydict


class SlugModelManager(models.Manager):
    def get(self, **kwargs):
        kwargs = _replace_slug(kwargs)
        return super(SlugModelManager, self).get(**kwargs)

    def filter(self, **kwargs):
        kwargs = _replace_slug(kwargs)
        return super(SlugModelManager, self).filter(**kwargs)


class SlugModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    objects = SlugModelManager()

    class Meta:
        abstract = True
        default_manager_name = 'objects'

    @cached_property
    def slug(self):
        return slugid.encode(self.uuid).decode('utf-8')