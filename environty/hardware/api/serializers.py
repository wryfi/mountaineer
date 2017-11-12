from rest_framework import serializers

from environty.hardware.models import Cabinet, CabinetAssignment, Datacenter, NetworkDevice, PortAssignment, PowerDistributionUnit, Server


class DeviceIdModelSerializer(serializers.HyperlinkedModelSerializer):
    device_id = serializers.SerializerMethodField()

    def get_device_id(self, obj):
        try:
            return obj.device.id
        except (AttributeError):
            return


class DatacenterSerializer(serializers.HyperlinkedModelSerializer):
    slug = serializers.ReadOnlyField()
    url = serializers.HyperlinkedIdentityField(view_name='api_v1:hardware:datacenter-detail', lookup_field='slug')

    class Meta:
        model = Datacenter
        fields = '__all__'


class CabinetSerializer(serializers.HyperlinkedModelSerializer):
    slug = serializers.ReadOnlyField()
    datacenter = serializers.HyperlinkedRelatedField(queryset=Datacenter.objects.all(), view_name='api_v1:hardware:datacenter-detail', lookup_field='slug')
    url = serializers.HyperlinkedIdentityField(view_name='api_v1:hardware:cabinet-detail', lookup_field='slug')

    class Meta:
        model = Cabinet
        fields = '__all__'


class CabinetAssignmentSerializer(DeviceIdModelSerializer):
    cabinet = serializers.HyperlinkedRelatedField(queryset=Cabinet.objects.all(), view_name='api_v1:hardware:cabinet-detail', lookup_field='slug')
    depth = serializers.SerializerMethodField()
    orientation = serializers.SerializerMethodField()
    device_name = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='api_v1:hardware:cabinetassignment-detail', lookup_field='slug')

    class Meta:
        model = CabinetAssignment
        exclude = ('device',)

    def get_depth(self, obj):
        if obj.depth:
            return obj.depth.value

    def get_device_name(self, obj):
        return obj.device.object.__str__()

    def get_orientation(self, obj):
        if obj.orientation:
            return obj.orientation.value


class ServerDetailSerializer(DeviceIdModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_v1:hardware:server-detail', lookup_field='slug')
    cabinet = serializers.HyperlinkedRelatedField(
        queryset=Cabinet.objects.all(), view_name='api_v1:hardware:cabinet-detail', lookup_field='slug'
    )

    class Meta:
        model = Server
        exclude = ('device',)


class PduSerializer(DeviceIdModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_v1:hardware:powerdistributionunit-detail', lookup_field='slug')
    watts = serializers.SerializerMethodField()
    cabinet = serializers.HyperlinkedRelatedField(
        queryset=Cabinet.objects.all(), view_name='api_v1:hardware:cabinet-detail', lookup_field='slug'
    )

    class Meta:
        model = PowerDistributionUnit
        exclude = ('device',)

    def get_watts(self, obj):
        return obj.watts


class NetworkDeviceSerializer(DeviceIdModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_v1:hardware:networkdevice-detail', lookup_field='slug')
    speed = serializers.SerializerMethodField()
    interconnect = serializers.SerializerMethodField()
    cabinet = serializers.HyperlinkedRelatedField(
        queryset=Cabinet.objects.all(), view_name='api_v1:hardware:cabinet-detail', lookup_field='slug'
    )

    class Meta:
        model = NetworkDevice
        exclude = ('device',)

    def get_speed(self, obj):
        if obj.speed:
           return obj.speed.value

    def get_interconnect(self, obj):
        if obj.interconnect:
            return obj.interconnect.value


class PortAssignmentSerializer(DeviceIdModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_v1:hardware:portassignment-detail', lookup_field='slug')
    connected_device = serializers.SerializerMethodField()

    class Meta:
        model = PortAssignment
        exclude = ('device',)

    def get_connected_device(self, obj):
        return obj.connected_device.id
