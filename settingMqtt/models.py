from django.db import models
import random
from django.contrib.auth.models import User

class SettingMqtt(models.Model):
    client_id = models.CharField(max_length=3)
    #client_id = models.CharField(primary_key=True, max_length=3)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    broker_ip = models.CharField(max_length=30)
    port = models.IntegerField()
    topic = models.CharField(max_length=60)
    #client_id = models.CharField(max_length=7, default=f'python-mqtt-{random.randint(0, 100)}', editable=False)
    username = models.CharField(max_length=30, default='emqx')
    password = models.CharField(max_length=30, default='public')
    message = models.CharField(max_length=60, default='', editable=False)


    def __str__(self):
        text = "{0} ({1})"
        return text.format(self.topic,self.broker_ip)
