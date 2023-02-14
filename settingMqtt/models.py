from django.db import models
from django.contrib.auth.models import User
from django.conf import settings 

class SettingMqtt(models.Model):
    client_id = models.CharField(max_length=3)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    broker_ip = models.CharField(max_length=30)
    port = models.IntegerField()
    topic = models.CharField(max_length=60)
    username = models.CharField(max_length=30, default='emqx')
    password = models.CharField(max_length=30, default='public')
    message = models.CharField(max_length=60, default='', editable=False)

    def __str__(self):
        text = "{0} ({1})"
        return text.format(self.topic,self.broker_ip)
