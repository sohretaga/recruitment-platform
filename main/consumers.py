from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
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
        async_to_sync(self.create_notification)(text_data)

        text_data_json = json.loads(text_data)
        message = text_data_json['content']

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'send_notification',
                'message': message,
            }
        )
    
    @database_sync_to_async
    def create_notification(self, text_data) -> None:
        from django.contrib.contenttypes.models import ContentType
        from job.models import Apply
        from main.models import Notification
        from user.models import CustomUser

        text_data_json = json.loads(text_data)
        related_data = text_data_json['related_data']
        content = text_data_json['content']

        related_object = dict()
        to_user = CustomUser.objects.get(id=self.target_user_id)

        if Apply.objects.filter(id=related_data).exists():
            apply = Apply.objects.get(id=related_data)
            apply_content_type = ContentType.objects.get_for_model(apply)

            related_object = {
                'content_type': apply_content_type,
                'object_id': apply.id
            }

        Notification.objects.create(
            from_user=self.user,
            to_user=to_user,
            content=content,
            read=False,
            **related_object
        )

    def send_notification(self, event):
        message = event['message']

        self.send(text_data=json.dumps(
            {'message': message}
        ))