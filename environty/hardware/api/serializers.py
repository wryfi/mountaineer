from rest_framework import serializers

from environty.hardware.models import Cabinet, CabinetAssignment, Datacenter, NetworkDevice, PortAssignment, PowerDistributionUnit, Server


class SlugModelSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    device_id = serializers.SerializerMethodField()

    class Meta:
        exclude = ('id', 'uuid')

    def get_device_id(self, obj):
        if obj.device:
            return obj.device.id


class DatacenterSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Datacenter
        exclude = ('id', 'uuid')


class CabinetSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Cabinet
        exclude = ('id', 'uuid')


class CabinetAssignmentSerializer(SlugModelSerializer):
    depth = serializers.SerializerMethodField()
    orientation = serializers.SerializerMethodField()

    class Meta:
        model = CabinetAssignment
        exclude = ('id', 'uuid')

    def get_depth(self, obj):
        if obj.depth:
            return obj.depth.value

    def get_orientation(self, obj):
        if obj.orientation:
            return obj.orientation.value


class ServerDetailSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    cabinet = serializers.SerializerMethodField()
    device_id = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()

    class Meta:
        model = Server
        exclude = ('device', 'id', 'uuid')

    def get_cabinet(self, obj):
        try:
            return obj.cabinet.name
        except AttributeError:
            return None

    def get_device_id(self, obj):
        return obj.device.id

    def get_position(self, obj):
        try:
            return obj.location[1]
        except (AttributeError, IndexError, TypeError):
            return None


class PduSerializer(SlugModelSerializer):
    watts = serializers.SerializerMethodField()

    class Meta:
        model = PowerDistributionUnit
        exclude = ('device', 'id', 'uuid')

    def get_watts(self, obj):
        return obj.watts


class NetworkDeviceSerializer(SlugModelSerializer):
    speed = serializers.SerializerMethodField()
    interconnect = serializers.SerializerMethodField()

    class Meta:
        model = NetworkDevice
        exclude = ('device', 'id', 'uuid')

    def get_speed(self, obj):
        if obj.speed:
           return obj.speed.value

    def get_interconnect(self, obj):
        if obj.interconnect:
            return obj.interconnect.value


class PortAssignmentSerializer(SlugModelSerializer):
    class Meta:
        model = PortAssignment
        exclude = ('device', 'id', 'uuid')