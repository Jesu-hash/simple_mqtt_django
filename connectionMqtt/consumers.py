import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings


class SystemConsumer(AsyncWebsocketConsumer):
    #group_name = settings.STREAM_SOCKET_GROUP_NAME
    # user = Account.objects.get(email__exact=email)
    # group_name = "group_"+user

    async def connect(self):
        # Joining group

        user_name = str(self.scope['session']['logged_user'])
        user_name = user_name.split("@")[0]
        group_name = user_name
        

        await self.channel_layer.group_add(
            group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave group
        user_name = str(self.scope['session']['logged_user'])
        user_name = user_name.split("@")[0]
        group_name = user_name

        await self.channel_layer.group_discard(
            group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Receive data from WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        # Print message that receive from Websocket

        user_name = str(self.scope['session']['logged_user'])
        user_name = user_name.split("@")[0]
        group_name = user_name

        # Send data to group
        await self.channel_layer.group_send(
            group_name,
            {
                'type': 'system_load',
                'data': {
                    'Id': 0,
                    'data': 0,
                    'timestamp': 0

                }
            }
        )

    async def system_load(self, event):
        # Receive data from group
        await self.send(text_data=json.dumps(event['data']))