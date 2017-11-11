from rest_framework import routers

from environty.hardware.api import viewsets


router = routers.SimpleRouter()
router.register(r'hardware/servers', viewsets.ServerModelViewSet)

urlpatterns = [
]
