from audioop import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

def home(request):
    #messages.success(request, '¡Listado conexiones!')
    return render(request,"home.html")

def about(request):

    about = "About me..."
    
    context= {'about': about}
        
    return render(request, 'about.html', context)

