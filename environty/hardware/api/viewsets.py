from environty.hardware.models import Cabinet, CabinetAssignment, Datacenter, NetworkDevice, PortAssignment, PowerDistributionUnit, Server
from environty.hardware.api.serializers import CabinetSerializer, CabinetAssignmentSerializer, DatacenterSerializer, NetworkDeviceSerializer, PduSerializer, PortAssignmentSerializer, ServerDetailSerializer
from environty.core.api.viewsets import SlugModelViewSet


class DatacenterModelViewSet(SlugModelViewSet):
    queryset = Datacenter.objects.all()
    serializer_class = DatacenterSerializer
    lookup_field = 'slug'


class CabinetModelViewSet(SlugModelViewSet):
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer
    lookup_field = 'slug'


class CabinetAssignmentModelViewSet(SlugModelViewSet):
    queryset = CabinetAssignment.objects.all()
    serializer_class = CabinetAssignmentSerializer


class ServerModelViewSet(SlugModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerDetailSerializer
    lookup_field = 'slug'


class PduModelViewSet(SlugModelViewSet):
    queryset = PowerDistributionUnit.objects.all()
    serializer_class = PduSerializer


class NetDeviceModelViewSet(SlugModelViewSet):
    queryset = NetworkDevice.objects.all()
    serializer_class = NetworkDeviceSerializer


class PortAssignmentModelViewSet(SlugModelViewSet):
    queryset = PortAssignment.objects.all()
    serializer_class = PortAssignmentSerializer