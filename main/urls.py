from django.urls import path
from . import views
from settingMqtt.views import mqttSetting
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    #path('',views.home),
    path('', views.welcome, name='welcome'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
	path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    #path('managementConnection/',mqttSetting, name="setting"),
    path('about/', views.about, name='about'),

]