from django.core.exceptions import ImproperlyConfigured
from django.conf.urls import include, url
from django.conf import settings

from mountaineer.core.api import views
from rest_framework_swagger.views import get_swagger_view


urlpatterns = [
    url(r'^$', views.v1_root, name='root'),
    url(r'^swagger/', get_swagger_view('api'))
]

if 'mntnr_hardware' in settings.INSTALLED_APPS:
    try:
        from mntnr_hardware.api import urls_v1 as hardware_urls
    except ImportError:
        raise ImproperlyConfigured('mntnr_hardware is in INSTALLED_APPS but does not appear to be installed')
    urlpatterns += [
        url(r'^hardware/', include(hardware_urls)),
    ]
