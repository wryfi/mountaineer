from mountaineer.hardware.models import (
    Cabinet, CabinetAssignment, Datacenter, NetworkDevice, PortAssignment, PowerDistributionUnit, Server
)
from mountaineer.hardware.api.serializers import (
    CabinetSerializer, CabinetAssignmentSerializer, DatacenterSerializer, NetworkDeviceSerializer,
    PduSerializer, PortAssignmentSerializer, ServerDetailSerializer
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #headers = self.get_success_headers(serializer.data)
        print(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ServerModelViewSet(SlugModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerDetailSerializer


class PduModelViewSet(SlugModelViewSet):
    queryset = PowerDistributionUnit.objects.all()
    serializer_class = PduSerializer


class NetDeviceModelViewSet(SlugModelViewSet):
    queryset = NetworkDevice.objects.all()
    serializer_class = NetworkDeviceSerializer


class PortAssignmentModelViewSet(SlugModelViewSet):
    queryset = PortAssignment.objects.all()
    serializer_class = PortAssignmentSerializer