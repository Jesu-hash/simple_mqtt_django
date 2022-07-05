from django.urls import path, re_path
from connectionMqtt.views import *

urlpatterns = [
    path('menuConnection/<pk>/',connect, name="connect"),
]

