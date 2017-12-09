from mountaineer.hardware.models import (
    Cabinet, CabinetAssignment, Datacenter, NetworkDevice, PortAssignment, PowerDistributionUnit, Server
)
from mountaineer.hardware.api.serializers import (
    CabinetSerializer, CabinetAssignmentSerializer, DatacenterSerializer, NetworkDeviceSerializer,
    PduSerializer, PortAssignmentSerializer, ServerSerializer
)
from rest_framework.viewsets import ModelViewSet
from rest_framework import response, status


class SlugModelViewSet(ModelViewSet):
    lookup_field = 'slug'


class DatacenterModelViewSet(SlugModelViewSet):
    queryset = Datacenter.objects.all()
    serializer_class = DatacenterSerializer


class CabinetModelViewSet(SlugModelViewSet):
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer


class CabinetAssignmentModelViewSet(SlugModelViewSet):
    queryset = CabinetAssignment.objects.all()
    serializer_class = CabinetAssignmentSerializer


class ServerModelViewSet(SlugModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer


class PduModelViewSet(SlugModelViewSet):
    queryset = PowerDistributionUnit.objects.all()
    serializer_class = PduSerializer


class NetDeviceModelViewSet(SlugModelViewSet):
    queryset = NetworkDevice.objects.all()
    serializer_class = NetworkDeviceSerializer


class PortAssignmentModelViewSet(SlugModelViewSet):
    queryset = PortAssignment.objects.all()
    serializer_class = PortAssignmentSerializer