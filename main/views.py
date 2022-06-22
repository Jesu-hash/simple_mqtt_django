from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm
#from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def welcome(request):
    #messages.success(request, '¡Listado conexiones!')
    return render(request,"welcome.html")

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			messages.success(request, f'Usuario {username} creado')
			return redirect('setting')
	else:
		form = UserRegisterForm()

	context = { 'form' : form }
	return render(request, 'register.html', context)

def about(request):

    about = "About me..."
    
    context= {'about': about}
        
    return render(request, 'about.html', context)

