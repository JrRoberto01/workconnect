from django.apps import apps
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user = self.scope['user']

        if user.is_authenticated:
            await self.save_message(self.room_name, user, message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': user.email,
                }
            )
        else:
            await self.send(text_data=json.dumps({
                'error': 'Usuário não autenticado'
            }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user': event['user']
        }))

    @sync_to_async
    def save_message(self, room_name, user, message):
        ChatRoom = apps.get_model('core', 'ChatRoom')
        Message = apps.get_model('core', 'Message')

        room = None

        if room_name.startswith("group_"):
            try:
                room_id = int(room_name.replace("group_", ""))
                room = ChatRoom.objects.get(id=room_id, is_group=True)
            except ChatRoom.DoesNotExist:
                print(f"ChatRoom with id {room_id} not found.")
                return
        else:
            ids = room_name.split("_")
            if len(ids) == 2:
                try:
                    user_ids = [int(i) for i in ids]
                    all_rooms = ChatRoom.objects.filter(is_group=False)
                    for r in all_rooms:
                        participantes = list(r.participants.values_list('id', flat=True))
                        if sorted(participantes) == sorted(user_ids):
                            room = r
                            break
                except ValueError:
                    print(f"Invalid user IDs in room_name: {room_name}")
                    return


        if room:
            Message.objects.create(
                room=room,
                sender=user,
                content=message
            )
        else:
            print(f"Room not found or determined for room_name: {room_name}")