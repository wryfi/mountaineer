from rest_framework import routers

from environty.hardware.api import viewsets


router = routers.SimpleRouter()
router.register(r'hardware/cabinets', viewsets.CabinetModelViewSet)
router.register(r'hardware/cabinet-assignments', viewsets.CabinetAssignmentModelViewSet)
router.register(r'hardware/datacenters', viewsets.DatacenterModelViewSet)
router.register(r'hardware/network', viewsets.NetDeviceModelViewSet)
router.register(r'hardware/pdus', viewsets.PduModelViewSet)
router.register(r'hardware/port-assignments', viewsets.PortAssignmentModelViewSet)
router.register(r'hardware/servers', viewsets.ServerModelViewSet)

urlpatterns = [
]
