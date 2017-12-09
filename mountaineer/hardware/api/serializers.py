from rest_framework import serializers

from mountaineer.core.api import fields as mtnr_fields
from mountaineer.core.utils import slug
from mountaineer.hardware import (
    RackDepth, RackOrientation, SwitchSpeed, SwitchInterconnect, CabinetAttachmentMethod, CabinetFastener
)
from mountaineer.hardware.api import fields as hw_fields
from mountaineer.hardware.models import (
    Cabinet, CabinetAssignment, Datacenter, NetworkDevice, PortAssignment, PowerDistributionUnit, Server
)


MODEL_VIEW_MAPS = {
    PowerDistributionUnit: 'api_v1:hardware:powerdistributionunit-detail',
    Server: 'api_v1:hardware:server-detail',
    NetworkDevice: 'api_v1:hardware:networkdevice-detail'
}


class DeviceIdModelSerializer(serializers.HyperlinkedModelSerializer):
    device_id = serializers.SerializerMethodField()

    def get_device_id(self, obj):
        try:
            return obj.device.id
        except (AttributeError):
            return


class DatacenterSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_v1:hardware:datacenter-detail', lookup_field='slug')
    slug = serializers.CharField(read_only=True, default=slug.slugid_nice())

    class Meta:
        model = Datacenter
        fields = '__all__'


class CabinetSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_v1:hardware:cabinet-detail', lookup_field='slug')
    slug = serializers.CharField(read_only=True, default=slug.slugid_nice())
    datacenter = serializers.HyperlinkedRelatedField(
        queryset=Datacenter.objects.all(), view_name='api_v1:hardware:datacenter-detail', lookup_field='slug'
    )
    attachment = mtnr_fields.SerializerEnumField(enum=CabinetAttachmentMethod)
    fasteners = mtnr_fields.SerializerEnumField(enum=CabinetFastener)
    power = serializers.SerializerMethodField()
    power_allocated = serializers.SerializerMethodField()
    power_unallocated = serializers.SerializerMethodField()

    class Meta:
        model = Cabinet
        fields = '__all__'

    def get_power(self, obj):
        return obj.power

    def get_power_allocated(self, obj):
        return obj.power_allocated

    def get_power_unallocated(self, obj):
        return obj.power_unallocated


class CabinetAssignmentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api_v1:hardware:cabinetassignment-detail', lookup_field='slug'
    )
    slug = serializers.CharField(read_only=True, default=slug.slugid_nice())
    cabinet = serializers.HyperlinkedRelatedField(
        queryset=Cabinet.objects.all(), view_name='api_v1:hardware:cabinet-detail', lookup_field='slug'
    )
    cabinet_name = serializers.SerializerMethodField()
    device = hw_fields.HyperlinkedDeviceField(lookup_field='slug', read_only=True, model_view_maps=MODEL_VIEW_MAPS)
    device_id = serializers.UUIDField()
    device_name = serializers.SerializerMethodField()
    depth = mtnr_fields.SerializerEnumField(enum=RackDepth)
    orientation = mtnr_fields.SerializerEnumField(enum=RackOrientation)

    class Meta:
        model = CabinetAssignment
        fields = '__all__'

    def get_cabinet_name(self, obj):
        return obj.cabinet.name

    def get_device_name(self, obj):
        return obj.device.instance.__str__()


class ServerSerializer(DeviceIdModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_v1:hardware:server-detail', lookup_field='slug')
    cabinet = serializers.HyperlinkedRelatedField(
        view_name='api_v1:hardware:cabinet-detail', lookup_field='slug', read_only=True
    )

    class Meta:
        model = Server
        exclude = ('device',)


class PduSerializer(DeviceIdModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api_v1:hardware:powerdistributionunit-detail', lookup_field='slug'
    )
    watts = serializers.SerializerMethodField()
    cabinet = serializers.HyperlinkedRelatedField(
        view_name='api_v1:hardware:cabinet-detail', lookup_field='slug', read_only=True
    )

    class Meta:
        model = PowerDistributionUnit
        exclude = ('device',)

    def get_watts(self, obj):
        return obj.watts


class NetworkDeviceSerializer(DeviceIdModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_v1:hardware:networkdevice-detail', lookup_field='slug')
    speed = mtnr_fields.SerializerEnumField(enum=SwitchSpeed)
    interconnect = mtnr_fields.SerializerEnumField(enum=SwitchInterconnect)
    cabinet = serializers.HyperlinkedRelatedField(
        view_name='api_v1:hardware:cabinet-detail', lookup_field='slug', read_only=True
    )

    class Meta:
        model = NetworkDevice
        exclude = ('device',)


class PortAssignmentSerializer(DeviceIdModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_v1:hardware:portassignment-detail', lookup_field='slug')
    device = hw_fields.HyperlinkedDeviceField(lookup_field='slug', read_only=True, model_view_maps=MODEL_VIEW_MAPS)
    device_id = serializers.UUIDField()
    device_name = serializers.SerializerMethodField()
    device_port = serializers.IntegerField()
    connected_device = hw_fields.HyperlinkedDeviceField(lookup_field='slug', read_only=True,
                                                          model_view_maps=MODEL_VIEW_MAPS)
    connected_device_id = serializers.UUIDField()
    connected_device_name = serializers.SerializerMethodField()

    class Meta:
        model = PortAssignment
        fields = '__all__'

    def get_device_name(self, obj):
        return obj.device.instance.__str__()

    def get_connected_device_name(self, obj):
        return obj.connected_device.instance.__str__()
