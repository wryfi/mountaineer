from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def v1_root(request, format=None):
    return Response({
        'hardware': reverse('api_v1:hardware-root', request=request, format=format),
    })


@api_view(['GET'])
def root(request, format=None):
    return Response({
        'v1': reverse('api_v1:root', request=request, format=format),
    })
