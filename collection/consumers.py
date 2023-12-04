import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class MsgConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.room_group_name = "default"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        pass

    def receive(self, text_data=None, bytes_data=None):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "message", "message": text_data}
        )

    def message(self, event):
        message = event["message"]

        self.send(text_data=json.dumps({"type": "message", "message": message}))
