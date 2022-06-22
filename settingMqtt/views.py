from ast import SetComp
from email import message
from django.shortcuts import render, redirect
from .models import SettingMqtt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def mqttSetting(request):

    mqtt_connection_data = SettingMqtt.objects.filter(user_id=request.user.id)

    messages.success(request, '¡Listado conexiones!')
    return render(request,"managementConnection.html", {"connections":mqtt_connection_data})

@login_required
def mqttRegister(request, user):
    client_id = request.POST['txtClient_id']
    broker_ip = request.POST['txtBroker_ip']
    port = request.POST['numPort']
    topic = request.POST['txtTopic']
    username = request.POST['txtUsername']
    password = request.POST['txtPassword']
    message = request.POST['txtMessage']

    user = User.objects.get(username=user)

    SettingMqtt.autor = user.id

    connection = SettingMqtt.objects.create(user_id=user.id,client_id=client_id, broker_ip=broker_ip, port=port, topic=topic, username=username, password=password, message=message)

    messages.success(request, '¡Conexion registrada!')

    return redirect('setting')

@login_required
def deleteConnection(request, client_id):
    connection = SettingMqtt.objects.get(client_id=client_id)
    connection.delete()

    messages.success(request, '¡Conexion eliminada!')

    return redirect('setting')

@login_required
def editionConnection(request, client_id):
    connection = SettingMqtt.objects.get(client_id=client_id)
    return render(request, "editConnection.html", {"connection":connection})

@login_required
def editConnection(request):
    client_id = request.POST['txtClient_id']
    broker_ip = request.POST['txtBroker_ip']
    port = request.POST['numPort']
    topic = request.POST['txtTopic']
    username = request.POST['txtUsername']
    password = request.POST['txtPassword']
    message = request.POST['txtMessage']

    connection = SettingMqtt.objects.get(client_id=client_id)

    connection.client_id = client_id
    connection.broker_ip = broker_ip
    connection.port = port
    connection.topic = topic
    connection.username = username
    connection.password = password
    connection.message = message

    connection.save()
    messages.success(request, '¡Conexion actualizada!')
    return redirect('setting')
