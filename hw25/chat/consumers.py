import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Consumer handling real-time WebSocket communication.
    Tracks active connections, broadcasts chat messages, and triggers push notifications.
    """

    connected_channels = set()

    async def connect(self) -> None:
        """
        Accepts the connection, joins the global room group, and broadcasts the updated online user count.
        :return: None
        """
        self.room_group_name = "global_room"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        self.connected_channels.add(self.channel_name)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'online_count_update',
                'count': len(self.connected_channels)
            }
        )

    async def disconnect(self, close_code: int) -> None:
        """
        Removes the channel from active connections and the group, then broadcasts the updated online user count.
        :param close_code: WebSocket close code indicating the reason for closure
        :return: None
        """
        self.connected_channels.discard(self.channel_name)

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'online_count_update',
                'count': len(self.connected_channels)
            }
        )

    async def receive(self, text_data: str) -> None:
        """
        Receives messages from the client.
        Enforces authentication for chat messages and handles push notification requests.
        :param text_data: raw JSON payload received from the client
        :return: None
        """
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        msg_type = data.get('type')
        message = data.get('message', '').strip()

        if not message:
            return

        user = self.scope.get('user')

        if msg_type == 'chat_message':
            if not user or not user.is_authenticated:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'Guests are not allowed to send chat messages.'
                }))
                return

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message_broadcast',
                    'username': user.username,
                    'message': message
                }
            )

        elif msg_type == 'push_notification':
            sender = user.username if user and user.is_authenticated else "Guest"
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'push_notification_broadcast',
                    'sender': sender,
                    'message': message
                }
            )

    async def chat_message_broadcast(self, event: dict) -> None:
        """
        Broadcasts a chat message to the client.
        :param event: dictionary containing the username of the sender and the message text
        :return: None
        """
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'username': event['username'],
            'message': event['message']
        }))

    async def push_notification_broadcast(self, event: dict) -> None:
        """
        Broadcasts a push notification to the client.
        :param event: dictionary containing the sender name and the notification message
        :return: None
        """
        await self.send(text_data=json.dumps({
            'type': 'push_notification',
            'sender': event['sender'],
            'message': event['message']
        }))

    async def online_count_update(self, event: dict) -> None:
        """
        Broadcasts the current online user count to the client.
        :param event: dictionary containing the active online count
        :return: None
        """
        await self.send(text_data=json.dumps({
            'type': 'online_count',
            'count': event['count']
        }))
