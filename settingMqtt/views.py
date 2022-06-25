from ast import SetComp
from email import message
from django.shortcuts import render, redirect
from .models import SettingMqtt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def mqttSetting(request):

    if request.method == "GET":
        mqtt_connection_data = SettingMqtt.objects.filter(user_id=request.user.id)

        return render(request,"managementConnection.html", {"connections":mqtt_connection_data})
    else:
        messages.ERROR(request, '¡No conozco ese método para esta request!')
        
@login_required
def createConnection(request, user):
    if request.method == "POST":

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

    else:
        messages.ERROR(request, '¡No conozco ese método para esta request!')

@login_required
def deleteConnection(request, client_id):
    if request.method == "GET":
        connection = SettingMqtt.objects.get(client_id=client_id)
        if connection:
            connection.delete()
            messages.success(request, '¡Conexion eliminada!')
        return redirect('setting')
    else:
        messages.ERROR(request, '¡No conozco ese método para esta request!')

@login_required
def editConnection(request, client=''):
    if request.method == "POST":
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

    elif request.method == "GET":
        print(client)
        connection = SettingMqtt.objects.get(client_id=client)
        return render(request, "editConnection.html", {"connection":connection})
    else:
        messages.ERROR(request, '¡No conozco ese método para esta request!')

