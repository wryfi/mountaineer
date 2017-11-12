from django.conf.urls import include, url

from environty.hardware.api import urls_v1 as hardware_urls
from environty.core.api import views


urlpatterns = [
    url(r'^$', views.v1_root, name='root'),
    url(r'^hardware/', include(hardware_urls)),
]
