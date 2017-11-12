import uuid

from django.utils.functional import cached_property
from enumfields import EnumIntegerField
from django.db import models

from environty.hardware import CpuManufacturer, RackDepth, RackOrientation, SwitchInterconnect, SwitchSpeed
from environty.core.models import SlugModel, SlugField


class Datacenter(SlugModel):
    name = models.CharField(max_length=256)
    vendor = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    noc_phone = models.CharField(max_length=24, blank=True)
    noc_email = models.EmailField(blank=True)
    noc_url = models.URLField(blank=True)

    def __str__(self):
       return 'datacenter: {}'.format(self.name)


class Cabinet(SlugModel):
    name = models.CharField(max_length=256)
    datacenter = models.ForeignKey('Datacenter')
    rack_units = models.PositiveIntegerField(help_text='Height of rack in Rack Units')
    posts = models.PositiveIntegerField(help_text='Number of posts in the rack (usually 2 or 4)')

    def __str__(self):
        return 'cabinet: {}'.format(self.name)

    @cached_property
    def power(self):
        watts = 0
        assignments = CabinetAssignment.objects.filter(cabinet=self)
        pdus = [assign.device.object for assign in assignments if assign.device.type == PowerDistributionUnit]
        for pdu in pdus:
            watts += pdu.watts
        return watts

    @cached_property
    def power_available(self):
        return self.power - self.power_allocated

    @cached_property
    def power_allocated(self):
        draw = 0
        assignments = CabinetAssignment.objects.filter(cabinet=self)
        for assign in assignments:
            device = assign.device.object
            if device.draw:
                draw += device.draw
        return draw

    @cached_property
    def devices(self):
        assignments = CabinetAssignment.objects.filter(cabinet=self)
        return [(assign.device.object, assign.position) for assign in assignments]


class CabinetAssignment(SlugModel):
    cabinet = models.ForeignKey('Cabinet')
    position = models.PositiveIntegerField(blank=True, null=True)
    orientation = EnumIntegerField(RackOrientation, blank=True, null=True)
    depth = EnumIntegerField(RackDepth, blank=True, null=True)
    device = models.OneToOneField('Device')

    def __str__(self):
        return '{}: {} in position {}'.format(
            self.cabinet.name,
            self.device,
            self.position
        )


class Device(models.Model):
    """
    To avoid using generic foreign keys, each of our devices will have a OneToOne
    relationship with an instance of this model. This is similar to Django's concrete
    model inheritance, but without the automatic joins added by the Django ORM.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        for attr in ['server', 'powerdistributionunit', 'networkdevice']:
            if hasattr(self, attr):
                return getattr(self, attr).__str__()

    @cached_property
    def object(self):
        for attr in ['server', 'powerdistributionunit', 'networkdevice']:
            if hasattr(self, attr):
                return getattr(self, attr)

    @cached_property
    def type(self):
        for attr in ['server', 'powerdistributionunit', 'networkdevice']:
            if hasattr(self, attr):
                return type(getattr(self, attr))


class DeviceBase(models.Model):
    manufacturer = models.CharField(max_length=128)
    model = models.CharField(max_length=128)
    serial = models.CharField(max_length=256)
    asset_id = models.CharField(max_length=64, blank=True, help_text='ID in external asset database, if any.')
    asset_tag = models.CharField(max_length=128, blank=True, help_text='Asset tag, if any.')
    rack_units = models.IntegerField(blank=True, null=True, help_text='Height of the device, in Rack Units')
    draw = models.PositiveIntegerField(blank=True, null=True, help_text='Power draw of the device, in Watts')
    device = models.OneToOneField('Device', on_delete=models.CASCADE, null=True, blank=True, editable=False)

    class Meta:
        abstract = True
        unique_together = ('manufacturer', 'model', 'serial')

    def __str__(self):
        return '{} {} #{}'.format(self.manufacturer, self.model, self.serial)

    @cached_property
    def cabinet(self):
        try:
            return self.device.cabinetassignment.cabinet
        except CabinetAssignment.DoesNotExist:
            return None

    def delete(self, *args, **kwargs):
        self.device.delete()
        super(DeviceBase, self).delete(*args, **kwargs)

    @cached_property
    def location(self):
        try:
            assignment = self.device.cabinetassignment
            return assignment.cabinet, assignment.position
        except CabinetAssignment.DoesNotExist:
            return None

    @cached_property
    def pdus(self):
        assignments = PortAssignment.objects.filter(connected_device=self.device)
        return [(assign.device.object, assign.device_port) for assign in assignments if assign.device.type == PowerDistributionUnit]

    def save(self, *args, **kwargs):
        if not self.device:
            self.device = Device.objects.create()
        super(DeviceBase, self).save(*args, **kwargs)

    @cached_property
    def uplinks(self):
        assignments = PortAssignment.objects.filter(connected_device=self.device)
        return [(assign.device.object, assign.device_port) for assign in assignments if assign.device.type == NetworkDevice]


class Server(DeviceBase, SlugModel):
    memory = models.PositiveIntegerField(blank=True, null=True, help_text='Physical RAM in MiB')
    cores = models.PositiveIntegerField(blank=True, null=True, help_text='Number of CPU cores')


class PortDeviceMixin(models.Model):
    ports = models.PositiveIntegerField(help_text='Number of ports available on the device')

    class Meta:
        abstract = True

    @cached_property
    def ports_available(self):
        start_ports = [port for port in range(1, self.ports + 1)]
        used_ports = self.ports_used
        return [port for port in start_ports if port not in used_ports]

    @cached_property
    def ports_used(self):
        assignments = PortAssignment.objects.filter(device=self.device)
        return [assign.device_port for assign in assignments]

    @cached_property
    def devices(self):
        assignments = PortAssignment.objects.filter(device=self.device)
        return [(assign.connected_device.object, assign.device_port) for assign in assignments]


class PowerDistributionUnit(PortDeviceMixin, DeviceBase, SlugModel):
    volts = models.PositiveIntegerField(help_text='Rated output voltage')
    amps = models.PositiveIntegerField(help_text='Rated output amperage')

    @cached_property
    def watts(self):
        return self.amps * self.volts


class NetworkDevice(PortDeviceMixin, DeviceBase, SlugModel):
    speed = EnumIntegerField(SwitchSpeed)
    interconnect = EnumIntegerField(SwitchInterconnect)


class PortAssignment(SlugModel):
    device = models.ForeignKey('Device', help_text='The device (e.g. switch or pdu) being connected to.')
    device_port = models.PositiveIntegerField()
    connected_device = models.ForeignKey('Device', help_text='The device being connected.', related_name='connected_device')

    class Meta:
        unique_together = ('device', 'device_port')

    def __str__(self):
        return '{} port {} < {}'.format(self.device, self.device_port, self.connected_device.object)

    def save(self, *args, **kwargs):
        if self.device_port not in self.device.object.ports_available:
            raise RuntimeError('Requested port is unavailable')
        super(PortAssignment, self).save(*args, **kwargs)
