from channels.generic.websocket import AsyncWebsocketConsumer
import json

from sk_python_proj.sk_python_project.models import Notification


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.group_name = f"notifications_{self.user.id}"
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
            unread_count = await self.get_unread_count()
            await self.send(text_data=json.dumps({
                'type': 'initial_count',
                'unread_count': unread_count
            }))
        else:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def get_unread_count(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = await User.objects.aget(pk=self.user.id)
        return await user.notifications.filter(is_read=False).acount()

    async def send_notification(self, event):
        unread_count = await self.get_unread_count()
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'unread_count': unread_count,
            'message': event.get('message', ''),
            'text': event.get('text', ''),
            'topic': event.get('topic', '')
        }))