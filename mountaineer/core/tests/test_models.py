import uuid

from mountaineer.core.tests import ModelMixinTestCase
from mountaineer.core import models


class SlugModelTests(ModelMixinTestCase):
    mixin = models.SlugModel

    def test_models_slugmodel_slug(self):
        test_instance = self.model.objects.create()
        self.assertTrue(hasattr(test_instance, 'slug'))

    def test_models_slugmodel_slug_cleans_to_uuid(self):
        test_instance = self.model.objects.create()
        test_instance.clean_fields()
        self.assertTrue(type(test_instance.slug) == uuid.UUID)

    def test_models_slugmodel_save_uuid_as_slug(self):
        test_instance = self.model.objects.create(slug=uuid.uuid4())
        self.assertIsInstance(test_instance.slug, uuid.UUID)
        test_instance.refresh_from_db()
        self.assertNotIsInstance(test_instance.slug, uuid.UUID)

    def test_models_slugmodel_filter_by_slug(self):
        test_instance = self.model.objects.create()
        slug = test_instance.slug
        self.assertIn(test_instance, self.model.objects.filter(slug=slug))

    def test_models_slugmodel_get_by_slug(self):
        test_instance = self.model.objects.create()
        slug = test_instance.slug
        self.assertEquals(test_instance, self.model.objects.get(slug=slug))
