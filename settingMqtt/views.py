from ast import Not, SetComp
from email import message
from django.shortcuts import render, redirect
from .models import SettingMqtt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from django.core.validators import validate_ipv46_address, RegexValidator

@login_required
def mqttSetting(request):

    if request.method == "GET":
        mqtt_connection_data = SettingMqtt.objects.filter(user_id=request.user.id)

        return render(request,"management_connection.html", {"connections":mqtt_connection_data})
    else:
        messages.error(request, '¡No conozco ese método para esta request!')
        
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

        validate_hostname = RegexValidator(regex=r'[a-zA-Z0-9-_]*\.[a-zA-Z]{2,6}')

        valid_ip = True
        valid_url = True
        digit_port = True
        try:
            validate_ipv46_address(broker_ip)
        except:
            valid_ip = False

        try:
            validate_hostname(broker_ip)
        except:
            valid_url = False

        if (not (port.isdigit()) ):
            digit_port = False

        invalid_port_or_broker = False
        if (not ( (valid_ip or valid_url) and (digit_port) ) ):
            print("---puerto i broker INcorrectos-----------")
            invalid_port_or_broker = True

        if (not(SettingMqtt.objects.filter(client_id=client_id).exists() or invalid_port_or_broker ) ):

            connection = SettingMqtt.objects.create(user_id=user.id,client_id=client_id, broker_ip=broker_ip, port=port, topic=topic, username=username, password=password, message=message)

            messages.success(request, '¡Conexion registrada!')
        else:
            messages.error(request, '¡Error en datos cargados!')
        
        return redirect('setting')

    else:
        messages.error(request, '¡No conozco ese método para esta request!')

@login_required
def deleteConnection(request, pk):
    if request.method == "GET":
        connection = SettingMqtt.objects.get(id=pk)
        if connection:
            connection.delete()
            messages.success(request, '¡Conexion eliminada!')
        return redirect('setting')
    else:
        messages.ERROR(request, '¡No conozco ese método para esta request!')

@login_required
def editConnection(request, pk=''):
    if request.method == "POST":
        client_id = request.POST['txtClient_id']
        broker_ip = request.POST['txtBroker_ip']
        port = request.POST['numPort']
        topic = request.POST['txtTopic']
        username = request.POST['txtUsername']
        password = request.POST['txtPassword']
        message = request.POST['txtMessage']

        connection = SettingMqtt.objects.get(id=pk)

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
        connection = SettingMqtt.objects.get(id=pk)
        return render(request, "edit_connection.html", {"connection":connection})
    else:
        messages.error(request, '¡No conozco ese método para esta request!')

