from django.urls import path
from . import views
#from connectionMqtt.views import connectConnection

urlpatterns = [
    path('management/',views.mqttSetting, name="setting"),
    path('create-connection/<user>',views.createConnection, name="createconnection"),
    path('edit-connection/<pk>/',views.editConnection, name="edition"),
    path('delete-connection/<pk>/',views.deleteConnection, name="delete"),
]