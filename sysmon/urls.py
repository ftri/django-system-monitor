from django.urls import path
from .views import sysmon_as_json


urlpatterns = [
    path('json/', sysmon_as_json, name="sysmon-json"),
    ]