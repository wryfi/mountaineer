import uuid
import slugid

from environty.core.utils.shortcuts import get_slug_or_404
from django.http import Http404
from environty.core.tests import ModelMixinTestCase
from environty.core import models
from django.core.exceptions import ObjectDoesNotExist


class SlugModelTests(ModelMixinTestCase):
    mixin = models.SlugModel

    def test_uuid_field(self):
        test_instance = self.model()
        self.assertEquals(type(test_instance.uuid), uuid.UUID)

    def test_slug_encode(self):
        test_instance = self.model()
        self.assertEquals(test_instance.slug, slugid.encode(test_instance.uuid).decode('utf-8'))

    def test_slug_decode(self):
        test_instance = self.model()
        self.assertEquals(test_instance.uuid, slugid.decode(test_instance.slug))

    def test_objects_manager(self):
        self.assertEquals(type(self.model.objects), models.SlugModelManager)

    def test_default_manager(self):
        self.assertEquals(type(self.model._default_manager), models.SlugModelManager)

    def test_replace_slug(self):
        test_dict = {'slug': 'HyR58xVdRyy3I1QwDUuaCw'}
        test_dict = models._replace_slug(test_dict)
        self.assertEquals(test_dict['uuid'], uuid.UUID('1f2479f3-155d-472c-b723-54300d4b9a0b'))

    def test_replace_invalid_slug(self):
        test_dict = {'slug': 'asdf1234'}
        with self.assertRaises(ObjectDoesNotExist):
            models._replace_slug(test_dict)

    def test_replace_slug_removed_slug(self):
        test_dict = {'slug': 'HyR58xVdRyy3I1QwDUuaCw'}
        test_dict = models._replace_slug(test_dict)
        self.assertFalse('slug' in test_dict.keys())

    def test_manager_get_by_slug(self):
        test_instance, created = self.model.objects.get_or_create()
        got = self.model.objects.get(slug=test_instance.slug)
        self.assertEquals(test_instance, got)

    def test_manager_get_bad_slug(self):
        with self.assertRaises(ObjectDoesNotExist):
            self.model.objects.get(slug='xxxxxxxxxxx')

    def test_get_slug_or_404_success(self):
        test_instance, created = self.model.objects.get_or_create()
        self.assertEquals(test_instance, get_slug_or_404(self.model, test_instance.slug))

    def test_get_slug_or_404_fail(self):
        with self.assertRaises(Http404):
            get_slug_or_404(self.model, 'yyyyyyyyyy')