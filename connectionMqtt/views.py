from audioop import reverse
#from datetime import time
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from settingMqtt.models import SettingMqtt
import json
from django.conf import settings
import threading
import paho.mqtt.client as mqtt
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render, redirect
import sys
import time
from django.http import JsonResponse

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
    def __init__(self, broker, port, timeout, topics, name):
        super(MqttClient, self).__init__()
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port
        self.timeout = timeout
        self.topics = topics
        self.name = name
        self.total_messages = 0

    def connect_to_broker(self):
        self.client.on_disconnect = self.on_disconnect
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker, self.port, self.timeout)
        #self.client.loop_forever()
        self.client.loop_start()

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        self.total_messages = self.total_messages + 1
        #print(str(msg.payload) + "Total: {}".format(self.total_messages))
        # print("INGRESE A on_message")
        # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic, client {self.name}")
        
        x = msg.payload.decode("utf-8")
        data = json.loads(x) # parse x:

        # for key, value in data['data'].items():
        #     print("key: ",key)
        #     print("value: ",value)

        # the result is a Python dictionary:
        draw_point(data)

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
             #client.connected_flag=True #set flag
             print("Connected to MQTT Broker! ", self.broker)    
             #send to client the boker and topics    
        else:
             client.loop_stop()  
             print("Failed to connect, return code %d\n", rc)

        #  Subscribe to a list of topics using a lock to guarantee that a topic is only subscribed once
        for topic in self.topics:
            client.subscribe(topic)

    def on_disconnect(self, client, userdata, rc):
        if rc == 0:
            print("client disconnected ok")
            client.connected_flag=False #set flag

    def on_publish(client, userdata, mid):
        time.sleep(1)
        print("In on_pub callback mid= "  ,mid)


clients = []
active_connections = False
@login_required
def connect(request):
    if request.method == "GET":

        global active_connections 
        clients_list=request.GET.getlist('clients[]')
        print("clients_list ", clients_list)

        global clients
        clients = create_connections(clients_list)

        no_threads=threading.active_count()
        print("Current threads =",no_threads)
        print("Creating  Connections ",len(clients)," clients")

        for i in range(len(clients)):

            #create new instance
            mqtt_client = MqttClient(clients[i]['broker'], clients[i]['port'], 60, [clients[i]['sub_topic']],clients[i]['name'])          
 
            clients[i]["client"]=mqtt_client
            clients[i]["client"].client.connected_flag=False #create flag in class

            try:
                clients[i]["client"].connect_to_broker()
                active_connections = True
            except:
                messages.error(request, '¡Connection Fialed to broker!')
                print("Connection Fialed to broker ",clients[i]["broker"])
                
                continue
                #return redirect('setting') 

            else:
                messages.success(request, 'Conexion MQTT establecida!')     
                print("Conexion MQTT establecida ",clients[i]["name"])
                clients[i]["client"].client.connected_flag=True

        no_threads=threading.active_count()
        print("current threads =",no_threads)

        return render(request,"menu_connection.html", {"clients":clients, "active_connections": active_connections})
 
    else:
        messages.error(request, '¡No conozco ese método para esta request!')

def create_connections(clients_ids):
    # clients_list=[
    # {"broker":"192.168.1.159","port":1883,"name":"blank","sub_topic":"test1","pub_topic":"test1"},
    # {"broker":"192.168.1.65","port":1883,"name":"blank","sub_topic":"test2","pub_topic":"test2"}
    # ]
    clients_list = []
    for i in range(len(clients_ids)):
        id = clients_ids[i]
        client = SettingMqtt.objects.get(client_id=id)

        dictTemp = {}  

        dictTemp['client_id'] = client.client_id
        dictTemp['broker'] = client.broker_ip
        dictTemp['sub_topic'] = client.topic
        dictTemp['port'] = client.port
        dictTemp['name'] = "client"+str(i)
        dictTemp['pub_topic'] = "sensores/nodo_10/public"
        dictTemp['user'] = ''
        dictTemp['password'] = ''

        clients_list.append(dictTemp)

    
    print("clients: ", clients_list)
    return clients_list   

def draw_point(data):

    group_name = settings.STREAM_SOCKET_GROUP_NAME
    channel_layer = get_channel_layer()
   
    async_to_sync(channel_layer.group_send)(
        group_name, {'type': 'system_load',  'data': data}

            )

@login_required
def disconnect(request):
    print("DISCONNECT------- ")
    if request.method == 'POST':
        slug = request.POST.get('slug', None)
        print("slug ", slug)
        
 
        for client in clients:
            #print("CLIENT ", client)
            client['client'].client.disconnect()
            client['client'].client.loop_stop()
        #allow time for allthreads to stop before existing
        time.sleep(2)

        for client in clients:
            print("CLIENT ", client['client'].client.connected_flag)

        no_threads=threading.active_count()
        print("current threads =",no_threads)

        return JsonResponse(
                        {
                            'content': {
                                'message': 'CLIENTES DESCONECTADOS',
                            }
                        }
                    )

@login_required
def publish(request):
    print("INGRESE A PUBLISH SERVER ",request.POST)
    if request.method == "POST":
  
        msg = request.POST.get('msg', None)
        client_id = request.POST.get('client_id', None)
        print("CLIENT ID: ", client_id)
        # msg = request.POST.get('my_publish_text')
        print("msg ", msg)

        for client in clients:
            if client["client_id"]==client_id:
                pub_topic=client["pub_topic"]

                if client["client"].client.connected_flag:
                    client["client"].client.publish(pub_topic,msg)
                    time.sleep(0.1)
                    print("publishing client "+ client["name"])
                    break

        return JsonResponse(
                {
                    'content': {
                        'message': 'Mensaje publicado correctamente',
                    }
                }
            )
    elif request.method == "GET":
        print('¡No se puede enviar metodo GET!')
        messages.error(request, '¡No se puede enviar metodo GET!')
        return redirect('connect')
    else:
        messages.error(request, '¡No conozco ese método para esta request!')
        print('¡No conozco ese método para esta request!')
        return redirect('connect')
