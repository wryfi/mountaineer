from django.conf.urls import include, url

from mountaineer.hardware.api import urls_v1 as hardware_urls
from mountaineer.core.api import views


urlpatterns = [
    url(r'^$', views.v1_root, name='root'),
    url(r'^hardware/', include(hardware_urls)),
]
