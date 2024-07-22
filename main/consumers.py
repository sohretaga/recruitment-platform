from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from main.models import Notification
from user.models import CustomUser
import json


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.target_user_id = self.scope["url_route"]["kwargs"]["id"]
        self.group_name = f'user-{self.target_user_id}'
        self.user = self.scope["user"]

        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )

    def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        to_user = CustomUser.objects.get(id=self.target_user_id)

        Notification.objects.create(
            from_user=self.user,
            to_user=to_user,
            content=message,
            read=False
        )

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'send_notification',
                'message': message,
            }
        )
    
    def send_notification(self, event):
        message = event['message']

        self.send(text_data=json.dumps(
            {'message': message}
        ))