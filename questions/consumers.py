# myapp/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer


class QuestionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        question_id = self.scope['url_route']['kwargs']['question_id']
        self.room_group_name = f"question_{question_id}"
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

    async def answer_created(self, event):
        await self.send(json.dumps(event));


    async def question_deleted(self, event):
        await self.send(json.dumps(event));

    async def answer_deleted(self, event):
        await self.send(json.dumps(event));