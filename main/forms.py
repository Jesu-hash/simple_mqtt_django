from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
	password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	password2 = forms.CharField(label='Confirma Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
		help_texts = {k:"" for k in fields }

	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))