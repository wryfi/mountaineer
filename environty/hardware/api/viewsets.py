from environty.hardware.models import Server
from environty.hardware.api.serializers import ServerDetailSerializer, ServerListSerializer
from environty.core.api.viewsets import SlugModelViewSet


class ServerModelViewSet(SlugModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerListSerializer
    lookup_field = 'slug'
