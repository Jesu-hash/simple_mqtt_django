from django.urls import path, re_path
from connectionMqtt.views import *

urlpatterns = [
    path('menu-connection/',connect, name="connect"),
    path('disconnect/', disconnect, name='disconnect'),
    path('publish/', publish, name='publish'),


]

