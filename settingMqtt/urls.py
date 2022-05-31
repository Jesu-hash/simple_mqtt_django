from django.urls import path
from . import views
from connectionMqtt.views import connectConnection

urlpatterns = [
    path('managementConnection/',views.mqttSetting, name="setting"),
    path('registerConnection/',views.mqttRegister),
    path('editionConnection/<client_id>',views.editionConnection, name="edition"),
    path('editConnection/',views.editConnection, name="edit"),
    path('deleteConnection/<client_id>',views.deleteConnection, name="delete"),
    path('menuConnection/',connectConnection, name="connect"),
]