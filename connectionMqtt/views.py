from audioop import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from settingMqtt.models import SettingMqtt
import json
from django.conf import settings
from threading import Thread
import paho.mqtt.client as mqtt
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render, redirect
import sys

# class MqttClient(Thread):
#     def __init__(self, broker, port, timeout, topics):
#         super(MqttClient, self).__init__()
#         self.client = mqtt.Client()
#         self.broker = broker
#         self.port = port
#         self.timeout = timeout
#         self.topics = topics
#         self.total_messages = 0

#     #  run method override from Thread class
#     def run(self):

#         try:
#             self.connect_to_broker()
#             #raise Exception('An error occured here.')
#         except Exception as e:
#             self.bucket.put(sys.exc_info())

#     def connect_to_broker(self):
#         self.client.on_connect = self.on_connect
#         self.client.on_message = self.on_message
#         self.client.connect(self.broker, self.port, self.timeout)
#         self.client.loop_forever()

#     # The callback for when a PUBLISH message is received from the server.
#     def on_message(self, client, userdata, msg):
#         self.total_messages = self.total_messages + 1
#         #print(str(msg.payload) + "Total: {}".format(self.total_messages))
#         #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        
#         x = msg.payload.decode("utf-8")
#         # parse x:
#         data = json.loads(x)
#         # the result is a Python dictionary:
#         draw_point(data)

#     # The callback for when the client receives a CONNACK response from the server.
#     def on_connect(self, client, userdata, flags, rc):
#         if rc == 0:
#              print("Connected to MQTT Broker!")
#         else:
#              print("Failed to connect, return code %d\n", rc)

#         #  Subscribe to a list of topics using a lock to guarantee that a topic is only subscribed once
#         for topic in self.topics:
#             client.subscribe(topic)







class MqttClient():
    def __init__(self, broker, port, timeout, topics):
        super(MqttClient, self).__init__()
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port
        self.timeout = timeout
        self.topics = topics
        self.total_messages = 0

    def connect_to_broker(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker, self.port, self.timeout)
        #self.client.loop_forever()
        self.client.loop_start()

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        self.total_messages = self.total_messages + 1
        #print(str(msg.payload) + "Total: {}".format(self.total_messages))
        #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        
        x = msg.payload.decode("utf-8")
        # parse x:
        data = json.loads(x)
        # the result is a Python dictionary:
        draw_point(data)

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
             print("Connected to MQTT Broker!")
        else:
             print("Failed to connect, return code %d\n", rc)

        #  Subscribe to a list of topics using a lock to guarantee that a topic is only subscribed once
        for topic in self.topics:
            client.subscribe(topic)


@login_required
def connect(request, pk):
    if request.method == "GET":

        connection = SettingMqtt.objects.get(id=pk)
        #MqttClient(connection.broker_ip, connection.port, 60, [connection.topic]).start()
        mqtt_client = MqttClient(connection.broker_ip, connection.port, 60, [connection.topic])

        try:
            mqtt_client.connect_to_broker()

        except Exception as e:
            print("ERROR CONNECT TO BROKER", e)
            messages.error(request, '¡ERROR CONNECT TO BROKER!')
            return redirect('setting') 

        else:
            messages.success(request, 'Conexion MQTT establecida!')     
            return render(request,"menuConnection.html", {"socketConnect":'websocket'})
 
    else:
        messages.ERROR(request, '¡No conozco ese método para esta request!')

def draw_point(data):

    id = int(data["Id"])
    temp = float(data["temp"])
    time_stamp = str(data["timestamp"])

    group_name = settings.STREAM_SOCKET_GROUP_NAME
    channel_layer = get_channel_layer()
   
    async_to_sync(channel_layer.group_send)(
        group_name,
            {
                'type': 'system_load',
                'data': {
                    'Id': id,
                    'temp': temp,
                    'timestamp': time_stamp

             }
                        }
            )

