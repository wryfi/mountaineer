from decimal import Decimal
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from mountaineer.hardware import models, CabinetAttachmentMethod, CabinetFastener
from mountaineer.hardware.api import serializers


class DatacenterSerializerTests(TestCase):
    def setUp(self):
        self.datacenter_attributes = {
            'name': 'test datacenter', 'vendor': 'hosting company', 'address': '123 fake st',
            'noc_phone': '+14155551212', 'noc_email': 'noc@hosting.co', 'noc_url': 'http://noc.hosting.co'
        }
        self.factory = RequestFactory()
        self.datacenter = models.Datacenter.objects.create(**self.datacenter_attributes)
        self.url = reverse('api_v1:hardware:datacenter-detail', kwargs={'slug': self.datacenter.slug})
        self.serializer = serializers.DatacenterSerializer(
            instance=self.datacenter, context={'request': self.factory.get(self.url)}
        )

    def test_contains_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(), ['url', 'slug', 'name', 'vendor', 'address', 'noc_phone', 'noc_email', 'noc_url']
        )

    def test_slug(self):
        data = self.serializer.data
        self.assertEqual(data['slug'], self.datacenter.slug)

    def test_url(self):
        data = self.serializer.data
        self.assertRegexpMatches(data['url'], '.*{}'.format(self.url))


class CabinetSerializerTests(TestCase):
    def setUp(self):
        datacenter = models.Datacenter.objects.create(name='name', vendor='vendor', address='123 fake st')
        self.cabinet_attributes = {
            'name': 'test cabinet', 'datacenter': datacenter, 'attachment': CabinetAttachmentMethod.CAGE_NUT_95,
            'rack_units': 42, 'posts': 4, 'width': Decimal(19.0), 'fasteners': CabinetFastener.UNF_10_32
        }
        self.factory = RequestFactory()
        self.cabinet = models.Cabinet.objects.create(**self.cabinet_attributes)
        self.url = reverse('api_v1:hardware:cabinet-detail', kwargs={'slug': self.cabinet.slug})
        self.serializer = serializers.CabinetSerializer(
            instance=self.cabinet, context={'request': self.factory.get(self.url)}
        )

    def test_contains_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(), [
                'name', 'slug', 'datacenter', 'rack_units', 'posts', 'depth', 'width', 'attachment', 'fasteners',
                'power', 'power_allocated', 'power_unallocated', 'url'
            ]
        )

    def test_slug(self):
        data = self.serializer.data
        self.assertEqual(data['slug'], self.cabinet.slug)

    def test_url(self):
        data = self.serializer.data
        self.assertRegexpMatches(data['url'], '.*{}'.format(self.url))

    def test_attachment(self):
        data = self.serializer.data
        self.assertEqual(data['attachment'], '9.5mm cage nut')

    def test_fastener(self):
        data = self.serializer.data
        self.assertEqual(data['fasteners'], 'UNF 10-32')
