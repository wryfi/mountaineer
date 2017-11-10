from django.contrib import admin
from django.apps import apps

from environty.hardware import models

for model in apps.get_app_config('hardware').get_models():
    if model != models.Device:
        admin.site.register(model)