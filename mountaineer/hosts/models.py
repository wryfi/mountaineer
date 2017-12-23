import uuid

from django.db import models
from django.utils.functional import cached_property
from enumfields import EnumIntegerField

from mountaineer.hardware.models import Device


class Host(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return 'host {}'.format(id)

    @cached_property
    def instance(self):
        pass

    @cached_property
    def type(self):
        pass


class HostBase(models.Model):
    hostname = models.Charfield(max_length=256, help_text='Fully qualified domain name', unique=True)
    environment = models.ForeigKey('Environment')
    roles = models.ManyToManyField('Role', blank=True)
    operating_system = EnumIntegerField(OperatingSystem)
    host = models.OneToOneField('Host', on_delete=models.CASCADE, null=True, blank=True, editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.hostname

    def delete(self, *args, **kwargs):
        self.host.delete()
        super(HostBase, self).delete(*args, **kwargs)

    @cached_property
    def domain(self):
        components = self.hostname.split('.')
        return '.'.join(components[1:])

    @cached_property
    def rolenames(self):
        return sorted([role.name for role in self.roles.all()])

    def save(self, *args, **kwargs):
        if not self.host:
            self.host = Host.objects.create()
        super(HostBase, self).save(*args, **kwargs)

    @cached_property
    def shortname(self):
        return self.hostname.split('.')[0]


class ClusterVirtualMachine(HostBase):
    parent = models.ForeignKey('Cluster')


class HostVirtualMachine(HostBase):
    parent = models.ForeignKey('DeviceHost')


class DeviceHost(HostBase):
    parent = models.ForeignKey(Device)
