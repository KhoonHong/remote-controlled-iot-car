# consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class MotionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def motion_detected(self):
        await self.send(text_data=json.dumps({
            'motion': 'detected'
        }))
