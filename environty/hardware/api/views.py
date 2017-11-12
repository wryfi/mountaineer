from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'cabinets': reverse('api_v1:hardware:cabinet-list', request=request, format=format),
        'cabinet-assignments': reverse('api_v1:hardware:cabinetassignment-list', request=request, format=format),
        'datacenters': reverse('api_v1:hardware:datacenter-list', request=request, format=format),
        'network': reverse('api_v1:hardware:networkdevice-list', request=request, format=format),
        'pdus': reverse('api_v1:hardware:powerdistributionunit-list', request=request, format=format),
        'port-assignments': reverse('api_v1:hardware:portassignment-list', request=request, format=format),
        'servers': reverse('api_v1:hardware:server-list', request=request, format=format),
    })
