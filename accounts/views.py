from django.shortcuts import render, redirect

#from connectionMqtt.views import add_window
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.conf import settings

import ctypes
import time

def register(request): 

    import connectionMqtt
    connectionMqtt.views.add_window(request)

    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password )
            #user.set_password(password)
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Por favor activa tu cuenta en Vaxi Drez'
            body = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, body, to=[to_email])
            send_email.send()

            #messages.success(request, 'Se registro el usuario exitosamente')
            return redirect('/accounts/login/?command=verification&email='+email)

            #return render(request, 'accounts/login.html')

    context = {
        'form': form
    }

    return render(request, 'accounts/register.html', context)

def login(request):
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print("email ", email)
        print("password ", password)

        user = auth.authenticate(email=email, password=password)

        print("user ",user)

        if user is not None:
            auth.login(request,user)

            email = str(user)
            username = email.split("@")[0]
            request.session['logged_user'] = username

            return redirect('home')
        else:
            messages.error(request, 'Las redenciales son incorrectas')
            return redirect('login')

    import connectionMqtt
    connectionMqtt.views.add_window(request)

    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    import connectionMqtt
    connectionMqtt.views.add_window(request)
    
    active_clients = request.session.get('active_clients', 0)
    settings.ACTIVE_CONNECTIONS -= active_clients

    clients = request.session.get('clients', [])

    for client in clients:
        if (client["connected_flag"]) == True:
            # get the value through memory address
            mqtt_client = ctypes.cast(client["address"], ctypes.py_object).value
            
            mqtt_client.client.disconnect()
            mqtt_client.client.loop_stop()
            time.sleep(1)
            client["connected_flag"]=False #create flag in class
      
    auth.logout(request)
    
    messages.success(request, 'Has salido de la sesión')

    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Felicidades, tu cuenta esta activa!')
        return redirect('login')
    else:
        messages.error(request, 'La activacion es invalida')
        return redirect('register')