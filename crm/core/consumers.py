import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

groups = ["echo_group"]


class WSConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, event):
        other_username = self.scope['user']
        print(other_username)
        print("connected", event)
        await self.channel_layer.group_add("echo_group", self.channel_name)
        await self.accept()

    async def stream(self, event):
        data = event["data"]
        if data['owner'] == self.scope['user'].username:
            print("stream", event)
            await self.send(json.dumps(data))

    async def new_order(self, event):
        data = event["data"]
        await self.send(json.dumps(data))
