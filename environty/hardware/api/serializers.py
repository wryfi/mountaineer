from rest_framework import serializers

from environty.hardware.models import NetworkDevice, PowerDistributionUnit, Server


class ServerListSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    cabinet = serializers.SerializerMethodField()

    class Meta:
        model = Server
        fields = ('slug', 'manufacturer', 'model', 'serial', 'cabinet', 'rack_units')

    def get_cabinet(self, obj):
        try:
            return obj.cabinet.name
        except AttributeError:
            return None


class ServerDetailSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    cabinet = serializers.SerializerMethodField()
    device_id = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()

    class Meta:
        model = Server
        exclude = ('device', 'uuid')

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
