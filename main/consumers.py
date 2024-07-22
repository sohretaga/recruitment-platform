from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["url_route"]["kwargs"]["id"]
        self.group_name = f'user-{self.user}'
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'employer_action_notification',
                'message': message,
            }
        )
    
    def employer_action_notification(self, event):
        message = text_data=event['message']

        self.send(text_data=json.dumps(
            {'message': message}
        ))