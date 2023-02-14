from audioop import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from connectionMqtt.views import add_window

def home(request):
    #messages.success(request, '¡Listado conexiones!')
    if not request.session.session_key:
            request.session.create()
            
    add_window(request)
    return render(request,"home.html")

def about(request):

    about = "About me..."
    
    context= {'about': about}

    add_window(request)    
    return render(request, 'about.html', context)

