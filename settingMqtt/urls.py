from django.urls import path
from . import views
from connectionMqtt.views import connectConnection

urlpatterns = [
    path('managementConnection/',views.mqttSetting, name="setting"),
    path('createConnection/<user>',views.createConnection, name="createconnection"),
    path('editConnection/<client>',views.editConnection, name="edition"),
    path('editConnection/',views.editConnection, name="edit"),
    path('deleteConnection/<client_id>',views.deleteConnection, name="delete"),
    path('menuConnection/',connectConnection, name="connect"),
]