from audioop import reverse

#from datetime import time
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.views import logout
from settingMqtt.models import SettingMqtt
import json
from django.conf import settings
import threading

import paho.mqtt.client as mqtt
from paho.mqtt.subscribeoptions import SubscribeOptions

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render, redirect
import time
from django.http import JsonResponse

import json
import ctypes

from django.views.decorators.csrf import csrf_exempt

class MqttClient():
    def __init__(self, broker, port, timeout, topics, name, group_name_to_send_msg):
        super(MqttClient, self).__init__()
        #mytransport = 'websockets' # or 'tcp'
        self.client = mqtt.Client()
        #self.client = mqtt.Client(protocol=mqtt.MQTTv311, clean_session=True)
        #self.client = mqtt.Client(client_id="myPy",transport=mytransport,protocol=mqtt.MQTTv5)
        #self.client = mqtt.Client(protocol=mqtt.MQTTv5)
        self.broker = broker
        self.port = port
        self.timeout = timeout
        self.topics = topics
        self.name = name
        self.total_messages = 0
        self.group_name_to_send_msg = group_name_to_send_msg

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
        print("INGRESO A ON MESSAGE")
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic, client {self.name}")
        
        x = msg.payload.decode("utf-8")
        data = json.loads(x) # parse x:

        # for key, value in data['data'].items():
        #     print("key: ",key)
        #     print("value: ",value)

        # the result is a Python dictionary:
        draw_point(data,self.group_name_to_send_msg)

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
        options = SubscribeOptions(qos=1, noLocal=True) #noLocal only working with MQTTv5
        
        for topic in self.topics:
            #client.subscribe(topic)
            client.subscribe(topic, options=options)

    def on_disconnect(self, client, userdata, rc):
        if rc == 0:
            print("client disconnected ok")
            client.connected_flag=False #set flag

    def on_publish(client, userdata, mid):
        time.sleep(1)
        print("In on_pub callback mid= "  ,mid)

active_connections = 0
@login_required
def connect(request):
    add_window(request)
    if request.method == "POST":

        active_connection = request.session.get('active_connection', False)

        if not active_connection:
            no_threads=threading.active_count()
            print("Current threads =",no_threads)
            #print("Creating  Connections ",len(request.session["clients"])," clients")

            global active_connections

            # Group name to websockets 
            user_name = str(request.session['logged_user'])
            user_name = user_name.split("@")[0]
            group_name_to_send_msg = user_name

            clients = request.session["clients"]
            for i in range(len(clients)):  
                #create new instance

                mqtt_client = MqttClient(clients[i]['broker'], clients[i]['port'], 60, [clients[i]['sub_topic']],clients[i]['name'],group_name_to_send_msg)          
                #mqtt_client.client.connected_flag=False #create flag in class     
                clients[i]["connected_flag"]=False #create flag in class  
    
                try:
                    mqtt_client.connect_to_broker()
               
                except:
                    broker = clients[i]["broker"]
                    messages.error(request, f"Connection Fialed to broker {broker}")
                    
                    continue
                else:
                    broker = clients[i]["broker"]
                    messages.success(request, f"Conexion MQTT establecida! {broker}")     
                    #mqtt_client.client.connected_flag=True
                    clients[i]["connected_flag"]=True #create flag in class
                    #request.session.modified = True
                    active_connections += 1
                    request.session['active_clients'] += 1
                    request.session['active_connection'] = True

                finally:
                    address = id(mqtt_client)
                    # display memory address
                    print("Memory address - ", address)             
                    
                    request.session["clients"][i]["address"] = address
                    request.session.modified = True

            settings.ACTIVE_CONNECTIONS = active_connections

            no_threads=threading.active_count()
            print("current threads =",no_threads)
  
            return render(request,"menu_connection.html", {"clients":request.session["clients"]})
        else:
            return render(request,"menu_connection.html", {"clients":request.session["clients"]})
 
    else:
        if request.session["clients"] is None:
            request.session["clients"] = []

        messages.error(request, '¡No conozco ese método para esta request!')
        return render(request,"menu_connection.html", {"clients":request.session["clients"]})

def create_connections(request):
    # clients_list=[
    # {"broker":"192.168.1.159","port":1883,"name":"blank","sub_topic":"test1","pub_topic":"test1"},
    # {"broker":"192.168.1.65","port":1883,"name":"blank","sub_topic":"test2","pub_topic":"test2"}
    # ]

    # if not request.session.session_key:
    #         request.session.create()
    add_window(request) 
    if request.method == "POST":

        request.session["clients"] = []
           
        clients_ids=request.POST.getlist('clients[]')
        print("clients_ids ", clients_ids)
    
        # request.session['clients'] 
        # request.session['active_clients'] 
        # request.session['logged_user'] 

        request.session['active_clients'] = 0
        request.session['active_connection'] = False
        # user_name = str(request.user)
        # request.session['logged_user'] = user_name

        # request.session.modified = True
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
            dictTemp['connected_flag'] = False        

            request.session["clients"].append(dictTemp)
  
        return render(request,"menu_connection.html", {"clients":request.session["clients"], "length": len(request.session["clients"])})
    else:
        clients = request.session.get('clients', '')
        if clients == '':
            request.session["clients"] = []

        return render(request,"menu_connection.html", {"clients":request.session["clients"], "length": len(request.session["clients"])})

def draw_point(data, group_name_to_send_msg):

    #group_name = settings.STREAM_SOCKET_GROUP_NAME
    channel_layer = get_channel_layer()
    group_name = group_name_to_send_msg

    async_to_sync(channel_layer.group_send)(
        group_name, {'type': 'system_load',  'data': data}

            )

@login_required
def disconnect(request):
    add_window(request)
    
    if request.method == 'POST':

        global active_connections

        print("active_connections ",active_connections)

        for client in request.session["clients"]:
            # get the value through memory address

            if (client["connected_flag"]) == True:
                mqtt_client = ctypes.cast(client["address"], ctypes.py_object).value
     
                active_connections = active_connections - 1 
                request.session['active_clients'] -= 1

                mqtt_client.client.disconnect()
                mqtt_client.client.loop_stop()
                time.sleep(1)

                client["connected_flag"]=False #create flag in class
        
        request.session['active_connection'] = False
        settings.ACTIVE_CONNECTIONS = active_connections

        #allow time for allthreads to stop before existing
        print("active_connections ",active_connections)
         
        no_threads=threading.active_count()
        print("current threads =",no_threads)

        return render(request,"menu_connection.html", {"clients":request.session["clients"]})

    elif request.method == "GET":
        messages.error(request, '¡No se puede enviar metodo GET!')
        return render(request,"menu_connection.html", {"clients":request.session["clients"]})
    else:
        messages.error(request, '¡No conozco ese método para esta request!')
        return render(request,"menu_connection.html", {"clients":request.session["clients"]})

@login_required
def publish(request):
    if request.method == "POST":
  
        msg = request.POST.get('msg', None)
        client_id = request.POST.get('client_id', None)
        
        for client in request.session["clients"]:
            if client["client_id"]==client_id:
                #sub_topic=client["sub_topic"]
                sub_topic=client["pub_topic"]       
                print("pub_topic ",client['pub_topic'])
                #print("pub_topic ",sub_topic)
 
                #if mqtt_client.client.connected_flag:
                if (client["connected_flag"]) == True:
                    mqtt_client = ctypes.cast(client["address"], ctypes.py_object).value

                    mqtt_client.client.publish(sub_topic,msg)
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
        messages.error(request, '¡No se puede enviar metodo GET!')
        return render(request,"menu_connection.html", {"clients":request.session["clients"]})
    else:
        messages.error(request, '¡No conozco ese método para esta request!')
        return render(request,"menu_connection.html", {"clients":request.session["clients"]})

@csrf_exempt
def close_browser(request):
    print("Se Cerro el browser antes",int(request.session['window_num']))
    window_num = int(request.session['window_num'])
    window_num -= 1
    request.session['window_num'] = str( window_num )
    print("Se Cerro el browser despues ",int(request.session['window_num']))
    
    if int( request.session['window_num'] ) == 0:
        print("CIERRE REAL")
        if request.user.is_authenticated:         
            logout(request) #calls out overridden log-out function  
        else:
            request.session.flush()
            # del request.session['window_num']
            # request.session.modified = True
    data = {}
    return JsonResponse(data)

# for every GET request Django increments the session variable
def add_window(request):
    print("SOY add_window ")
    if 'window_num' in list(request.session.keys()): #there are existing pages
        window_num = int(request.session['window_num'])
        window_num += 1 
        request.session['window_num'] = str( window_num )
    else: #first time load
        request.session['window_num'] = "1"