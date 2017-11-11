from django.conf.urls import include, url

from environty.hardware.api import urls_v1 as hardware_urls
from environty.core.api import routers

router = routers.ExtensibleRouter()
router.extend(hardware_urls.router)

urlpatterns = [
    url(r'^', include(router.urls)),
]