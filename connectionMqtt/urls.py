from django.urls import path, re_path
from connectionMqtt.views import *

urlpatterns = [
    path('menu-connection/',create_connections, name="create_connections"),
    path('connect/', connect, name='connect'),
    #path(r'^connect/$', connect, name='connect'),  
    path('disconnect/', disconnect, name='disconnect'),
    path('publish/', publish, name='publish'),


]

