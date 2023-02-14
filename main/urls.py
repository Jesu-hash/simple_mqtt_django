from django.urls import path
from . import views
from settingMqtt.views import mqttSetting
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    #path('',views.home),
    path('', views.home, name='home'),
	path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('about/', views.about, name='about'),

]