import uuid

from environty.core.tests import ModelMixinTestCase
from environty.core import models


class SlugModelTests(ModelMixinTestCase):
    mixin = models.SlugModel

    def test_slug(self):
        test_instance = self.model()
        self.assertTrue(hasattr(test_instance, 'slug'))

    def test_slug_cleans_to_uuid(self):
        test_instance = self.model()
        test_instance.clean_fields()
        self.assertTrue(type(test_instance.slug) == uuid.UUID)

    def test_save_uuid_as_slug(self):
        test_instance = self.model.objects.create(slug=uuid.uuid4())
        self.assertIsInstance(test_instance.slug, uuid.UUID)
        test_instance.refresh_from_db()
        self.assertNotIsInstance(test_instance.slug, uuid.UUID)

    def test_filter_by_slug(self):
        test_instance = self.model.objects.create()
        slug = test_instance.slug
        self.assertIn(test_instance, self.model.objects.filter(slug=slug))

    def test_get_by_slug(self):
        test_instance = self.model.objects.create()
        slug = test_instance.slug
        self.assertEquals(test_instance, self.model.objects.get(slug=slug))
