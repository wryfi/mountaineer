import json
from urllib import parse

from django.test import TestCase
from django.urls import reverse

from mountaineer.hardware.models import Cabinet, CabinetAssignment, Datacenter, Server


class DatacenterApiTests(TestCase):
    def setUp(self):
        self.dc1_attributes = {
            'name': 'dc1', 'vendor': 'hosting.com', 'address': '630 3rd St',
            'noc_phone': '+14157787700', 'noc_email': 'noc@hosting.com', 'noc_url': 'https://hosting.com'
        }
        self.dc2_attributes = {
            'name': 'dc2', 'vendor': 'hurricane electric', 'address': '48233 Warm Springs Blvd',
            'noc_phone': '+15105804100', 'noc_email': 'noc@he.net', 'noc_url': 'http://he.net'
        }
        self.dc3_attributes = {
            'name': 'dc3', 'vendor': 'equinix', 'address': '444 Toyoma Drive',
            'noc_phone': '+18663784649', 'noc_email': 'noc@equinix.com', 'noc_url': 'https://www.equinix.com'
        }
        self.dc1, _ = Datacenter.objects.get_or_create(**self.dc1_attributes)
        self.dc2, _ = Datacenter.objects.get_or_create(**self.dc2_attributes)
        self.create_read_url = reverse('api_v1:hardware:datacenter-list')
        self.read_update_delete_url = reverse('api_v1:hardware:datacenter-detail', kwargs={'slug': self.dc1.slug})

    def test_api_datacenter_detail(self):
        response = self.client.get(self.read_update_delete_url)
        data = response.json()
        url_path = parse.urlparse(data.pop('url')).path
        slug = data.pop('slug')
        self.assertEquals(self.dc1.slug, slug)
        self.assertEquals(reverse('api_v1:hardware:datacenter-detail', kwargs={'slug': self.dc1.slug}), url_path)
        self.assertEquals(data, self.dc1_attributes)

    def test_api_datacenter_create(self):
        response = self.client.post(self.create_read_url, self.dc3_attributes)
        data = response.json()
        url_path = parse.urlparse(data.pop('url')).path
        slug = data.pop('slug')
        self.assertEquals(reverse('api_v1:hardware:datacenter-detail', kwargs={'slug': slug}), url_path)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(data, self.dc3_attributes)

    def test_api_datacenter_list(self):
        response = self.client.get(self.create_read_url)
        names = [item['name'] for item in response.json()]
        self.assertEquals(len(response.json()), 2)
        self.assertIn('dc1', names)
        self.assertIn('dc2', names)

    def test_api_datacenter_delete(self):
        response = self.client.delete(self.read_update_delete_url)
        self.assertEquals(response.status_code, 204)
        self.assertEquals(Datacenter.objects.count(), 1)

    def test_api_datacenter_update(self):
        datacenter = self.client.get(self.read_update_delete_url, kwargs={'slug': self.dc1.slug}).json()
        datacenter['noc_phone'] = '+14155551212'
        response = self.client.put(self.read_update_delete_url, json.dumps(datacenter), content_type='application/json')
        data = response.json()
        self.assertEquals(data['noc_phone'], '+14155551212')


class CabinetApiTests(TestCase):
    def setUp(self):
        self.datacenter = Datacenter.objects.create(name='dc1', vendor='foo', address='123 fake st')
        self.datacenter_url = reverse('api_v1:hardware:datacenter-detail', kwargs={'slug': self.datacenter.slug})
        self.cab1_attributes = {
            'name': 'cabinet 1', 'rack_units': 42, 'posts': 4, 'depth': 96,
            'width': 19, 'attachment': 1, 'fasteners': 1, 'datacenter': self.datacenter
        }
        self.cab2_attributes = {
            'name': 'cabinet 2', 'rack_units': 42, 'posts': 4, 'depth': 192,
            'width': 19, 'attachment': 1, 'fasteners': 1, 'datacenter': self.datacenter
        }
        self.cab3_attributes = {
            'name': 'cabinet 3', 'rack_units': 42, 'posts': 4, 'depth': '128.125',
            'width': 19, 'attachment': 2, 'fasteners': 5, 'datacenter': self.datacenter
        }
        self.cab1, _ = Cabinet.objects.get_or_create(**self.cab1_attributes)
        self.cab2, _ = Cabinet.objects.get_or_create(**self.cab2_attributes)
        self.create_read_url = reverse('api_v1:hardware:cabinet-list')
        self.read_update_delete_url = reverse('api_v1:hardware:cabinet-detail', kwargs={'slug': self.cab1.slug})

    def test_api_cabinet_detail(self):
        response = self.client.get(self.read_update_delete_url)
        data = response.json()
        url_path = parse.urlparse(data.pop('url')).path
        datacenter_path = parse.urlparse(data.pop('datacenter')).path
        slug = data.pop('slug')
        expected = self.cab1_attributes.copy()
        expected.pop('datacenter')
        expected['power'], expected['power_allocated'], expected['power_unallocated'] = 0, 0, 0
        expected['attachment'] = '9.5mm cage nut'
        expected['fasteners'] = 'UNF 10-32'
        expected['depth'] = '96.000'
        expected['width'] = '19.000'
        self.assertEquals(self.cab1.slug, slug)
        self.assertEquals(
            reverse('api_v1:hardware:datacenter-detail', kwargs={'slug': self.datacenter.slug}),
            datacenter_path
        )
        self.assertEquals(reverse('api_v1:hardware:cabinet-detail', kwargs={'slug': slug}), url_path)
        self.assertEquals(data, expected)

    def test_api_cabinet_create(self):
        create_attrs = self.cab3_attributes.copy()
        create_attrs['datacenter'] = self.datacenter_url
        response = self.client.post(self.create_read_url, create_attrs)
        data = response.json()
        url_path = parse.urlparse(data.pop('url')).path
        datacenter_path = parse.urlparse(data.pop('datacenter')).path
        slug = data.pop('slug')
        expected = self.cab3_attributes.copy()
        expected.pop('datacenter')
        expected['power'], expected['power_allocated'], expected['power_unallocated'] = 0, 0, 0
        expected['attachment'] = 'direct attachment'
        expected['fasteners'] = 'M5'
        expected['depth'] = '128.125'
        expected['width'] = '19.000'
        self.assertEquals(response.status_code, 201)
        self.assertEquals(datacenter_path, self.datacenter_url)
        self.assertEquals(reverse('api_v1:hardware:cabinet-detail', kwargs={'slug': slug}), url_path)
        self.assertEquals(data, expected)

    def test_api_cabinet_list(self):
        response = self.client.get(self.create_read_url)
        names = [item['name'] for item in response.json()]
        self.assertEquals(len(response.json()), 2)
        self.assertIn('cabinet 1', names)
        self.assertIn('cabinet 2', names)

    def test_api_cabinet_delete(self):
        response = self.client.delete(self.read_update_delete_url)
        self.assertEquals(response.status_code, 204)
        self.assertEquals(Cabinet.objects.count(), 1)

    def test_api_cabinet_update(self):
        cabinet = self.client.get(self.read_update_delete_url, kwargs={'slug': self.cab1.slug}).json()
        cabinet['depth'] = '124.365'
        response = self.client.put(self.read_update_delete_url, json.dumps(cabinet), content_type='application/json')
        data = response.json()
        self.assertEquals(data['depth'], '124.365')


class CabinetAssignmentApiTests(TestCase):
    def setUp(self):
        self.datacenter, _ = Datacenter.objects.get_or_create(name='dc1', vendor='foo', address='123 fake st')
        self.cabinet, _ = Cabinet.objects.get_or_create(name='cab1', datacenter=self.datacenter, rack_units=42, posts=4)
        self.server1, _ = Server.objects.get_or_create(manufacturer='Dell', model='123', serial='456')
        self.server2, _ = Server.objects.get_or_create(manufacturer='Dell', model='123', serial='654')
        self.cabinet_url = reverse('api_v1:hardware:cabinet-detail', kwargs={'slug': self.cabinet.slug})
        self.server1_url = reverse('api_v1:hardware:server-detail', kwargs={'slug': self.server1.slug})
        self.server2_url = reverse('api_v1:hardware:server-detail', kwargs={'slug': self.server2.slug})
        self.assignment_attributes = {
            'cabinet': self.cabinet, 'device': self.server1.device, 'position': 13, 'depth': 4, 'orientation': 1
        }
        self.assignment, _ = CabinetAssignment.objects.get_or_create(**self.assignment_attributes)
        self.create_read_url = reverse('api_v1:hardware:cabinetassignment-list')
        self.read_update_delete_url = reverse(
            'api_v1:hardware:cabinetassignment-detail', kwargs={'slug': self.assignment.slug}
        )

    def test_api_cabinetassignment_detail(self):
        response = self.client.get(self.read_update_delete_url)
        data = response.json()
        url_path = parse.urlparse(data.pop('url')).path
        cabinet_path = parse.urlparse(data.pop('cabinet')).path
        device_path = parse.urlparse(data.pop('device')).path
        slug = data.pop('slug')
        self.assertEquals(cabinet_path, self.cabinet_url)
        self.assertEqual(slug, self.assignment.slug)
        self.assertEquals(device_path, self.server1_url)
        self.assertEquals(reverse('api_v1:hardware:cabinetassignment-detail', kwargs={'slug': slug}), url_path)
        self.assertEquals(data['cabinet_name'], self.cabinet.name)
        self.assertEquals(data['device_id'], str(self.server1.device.id))
        self.assertEquals(data['device_name'], self.server1.__str__())
        self.assertEquals(data['depth'], 'Full depth')
        self.assertEquals(data['orientation'], 'Front-facing')
        self.assertEquals(data['position'], self.assignment_attributes['position'])

    def test_api_cabinetassignment_create(self):
        create_attrs = {
            'cabinet': self.cabinet_url, 'device_id': self.server2.device.id,
            'position': 41, 'depth': 2, 'orientation': 2
        }
        response = self.client.post(self.create_read_url, create_attrs)
        data = response.json()
        cabinet_url = parse.urlparse(data.pop('cabinet')).path
        self.assertEquals(response.status_code, 201)
        self.assertEquals(cabinet_url, self.cabinet_url)
        self.assertEquals(data['device_id'], str(self.server2.device.id))
        self.assertEquals(data['position'], 41)
        self.assertEquals(data['depth'], 'Half depth')
        self.assertEquals(data['orientation'], 'Rear-facing')

    def test_api_cabinetassignment_list(self):
        response = self.client.get(self.create_read_url)
        slugs = [item['slug'] for item in response.json()]
        self.assertEquals(len(slugs), 1)
        self.assertIn(self.assignment.slug, slugs)

    def test_api_cabinetassignment_delete(self):
        response = self.client.delete(self.read_update_delete_url)
        self.assertEquals(response.status_code, 204)
        self.assertEquals(CabinetAssignment.objects.count(), 0)

    def test_api_cabinetassignment_update(self):
        assignment = self.client.get(self.read_update_delete_url, kwargs={'slug': self.assignment.slug}).json()
        assignment['position'] = 33
        response = self.client.put(self.read_update_delete_url, json.dumps(assignment), content_type='application/json')
        data = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(data['position'], 33)


class ServerApiTests(TestCase):
    pass

