from django.urls import path
from . import views
#from connectionMqtt.views import connectConnection

urlpatterns = [
    path('managementConnection/',views.mqttSetting, name="setting"),
    path('createConnection/<user>',views.createConnection, name="createconnection"),
    path('editConnection/<pk>/',views.editConnection, name="edition"),
    path('deleteConnection/<pk>/',views.deleteConnection, name="delete"),
    #path('menuConnection/<pk>/',connectConnection, name="connect"), 
]