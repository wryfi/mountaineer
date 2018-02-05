from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def root(request, fmt=None):
    return Response({
        'v1': reverse('api_v1:root', request=request, format=fmt),
    })


@api_view(['GET'])
def v1_root(request, fmt=None):
    root_navigation = {}
    if 'mntnr_hardware' in settings.INSTALLED_APPS:
        root_navigation['hardware'] = reverse('api_v1:hardware-root', request=request, format=fmt)
    return Response(root_navigation)
