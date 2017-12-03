from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase

from mountaineer.hardware.models import *


class CabinetTests(TestCase):
    def setUp(self):
        self.datacenter = Datacenter.objects.create(name='datacenter', vendor='vendor', address='122 fake st')
        self.cabinet = Cabinet.objects.create(name='cab1', datacenter=self.datacenter, rack_units=48, posts=4)
        self.pdu1 = PowerDistributionUnit.objects.create(manufacturer='apc', model='promillion', serial='123', ports=24, volts=208, amps=30)
        self.pdu2 = PowerDistributionUnit.objects.create(manufacturer='apc', model='promillion', serial='125', ports=24, volts=208, amps=30)
        self.pdu3 = PowerDistributionUnit.objects.create(manufacturer='apc', model='promillion', serial='129', ports=24, volts=208, amps=30)
        self.server = Server.objects.create(manufacturer='dell', model='xwhat', serial='432', draw=350)
        CabinetAssignment.objects.create(cabinet=self.cabinet, device=self.pdu1.device, position=1)
        CabinetAssignment.objects.create(cabinet=self.cabinet, device=self.pdu2.device, position=3)
        CabinetAssignment.objects.create(cabinet=self.cabinet, device=self.server.device, position=5)

    def test_power(self):
        self.assertEquals(self.cabinet.power, 12480)

    def test_power_used(self):
        self.assertEquals(self.cabinet.power_allocated, 350)

    def test_power_available(self):
        self.assertEquals(self.cabinet.power_available, 12480 - 350)

    def test_devices(self):
        self.assertIn((self.pdu1, 1), self.cabinet.devices)
        self.assertIn((self.pdu2, 3), self.cabinet.devices)
        self.assertIn((self.server, 5), self.cabinet.devices)
        self.assertNotIn(self.pdu3, [device[0] for device in self.cabinet.devices])


class DeviceTests(TestCase):
    def setUp(self):
        self.server = Server.objects.create(manufacturer='dell', model='foo', serial='1233', draw=350)
        self.pdu = PowerDistributionUnit.objects.create(manufacturer='apc', model='cpa', serial=142, ports=24, volts=208, amps=30)
        self.sw = NetworkDevice.objects.create(manufacturer='juniper', model='srx', serial=3523, ports=24, speed=1000, interconnect=1)

    def test_device(self):
        self.assertEquals(type(self.server.device), Device)
        self.assertEquals(self.server.device.type, Server)
        self.assertEquals(self.server.device.object, self.server)
        self.assertEquals(self.pdu.device.type, PowerDistributionUnit)
        self.assertEquals(self.pdu.device.object, self.pdu)
        self.assertEquals(self.sw.device.type, NetworkDevice)
        self.assertEquals(self.sw.device.object, self.sw)


class ServerTests(TestCase):
    def setUp(self):
        self.datacenter = Datacenter.objects.create(name='foo', vendor='foo', address='foo')
        self.cabinet = Cabinet.objects.create(name='cab', datacenter=self.datacenter, rack_units=48, posts=4)
        self.pdu = PowerDistributionUnit.objects.create(manufacturer='apc', model='cpa', serial=142, ports=24, volts=208, amps=30)
        self.sw = NetworkDevice.objects.create(manufacturer='juniper', model='srx', serial=3523, ports=24, speed=1000, interconnect=1)
        self.server = Server.objects.create(manufacturer='dell', model='foo', serial='1233', draw=350)
        CabinetAssignment.objects.create(cabinet=self.cabinet, device=self.server.device, position=35)
        PortAssignment.objects.create(device=self.pdu.device, device_port=5, connected_device=self.server.device)
        PortAssignment.objects.create(device=self.sw.device, device_port=5, connected_device=self.server.device)

    def test_cabinet(self):
        self.assertEquals(self.cabinet, self.server.cabinet)

    def test_location(self):
        self.assertEquals((self.cabinet, 35), self.server.location)

    def test_pdus(self):
        self.assertIn((self.pdu, 5), self.server.pdus)

    def test_uplinks(self):
        self.assertIn((self.sw, 5), self.server.uplinks)

    def test_save(self):
        self.assertEquals(type(self.server.device), Device)

    def test_unique_together(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Server.objects.create(manufacturer='dell', model='foo', serial='1233')
        Server.objects.create(manufacturer='dell', model='fo', serial='1233')
        Server.objects.create(manufacturer='del', model='foo', serial='1233')
        Server.objects.create(manufacturer='dell', model='foo', serial='1234')

    def test_delete(self):
        device = self.server.device
        self.server.delete()
        self.assertNotIn(device, Device.objects.all())
        self.assertEquals(0, len(CabinetAssignment.objects.filter(device=device)))
        self.assertEquals(0, len(PortAssignment.objects.filter(connected_device=device)))
        self.assertEquals(0, len(PortAssignment.objects.filter(device=device)))


class PduTests(TestCase):
    def setUp(self):
        self.pdu = PowerDistributionUnit.objects.create(manufacturer='apc', model='cpa', serial=142, ports=24, volts=208, amps=30)
        self.server = Server.objects.create(manufacturer='dell', model='foo', serial='1233', draw=350)
        PortAssignment.objects.create(device=self.pdu.device, device_port=5, connected_device=self.server.device)

    def test_ports_used(self):
        del self.pdu.ports_used
        self.assertEquals(1, len(self.pdu.ports_used))
        self.assertIn(5, self.pdu.ports_used)
        self.assertNotIn(1, self.pdu.ports_used)
        self.assertNotIn(25, self.pdu.ports_used)
        self.assertNotIn(0, self.pdu.ports_used)

    def test_ports_available(self):
        del self.pdu.ports_available
        del self.pdu.ports_used
        self.assertEquals(23, len(self.pdu.ports_available))
        self.assertNotIn(5, self.pdu.ports_available)
        self.assertNotIn(25, self.pdu.ports_available)
        self.assertNotIn(0, self.pdu.ports_available)

    def test_watts(self):
        self.assertEquals(6240, self.pdu.watts)


class TestPortAssignment(TestCase):
    def setUp(self):
        self.pdu = PowerDistributionUnit.objects.create(manufacturer='apc', model='cpa', serial=142, ports=24, volts=208, amps=30)
        self.server = Server.objects.create(manufacturer='dell', model='foo', serial='1233', draw=350)
        self.server2 = Server.objects.create(manufacturer='supermicro', model='light', serial='1351', draw=350)
        PortAssignment.objects.create(device=self.pdu.device, device_port=6, connected_device=self.server.device)

    def test_save_used_port(self):
        with self.assertRaises(IntegrityError):
            PortAssignment.objects.create(device=self.pdu.device, device_port=6, connected_device=self.server2.device)

    def test_save_outofrange_port(self):
        with self.assertRaises(RuntimeError):
            PortAssignment.objects.create(device=self.pdu.device, device_port=0, connected_device=self.server2.device)
