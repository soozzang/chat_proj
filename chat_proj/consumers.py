import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from chats.models import Room,ChatMessage,User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.roomGroupName = 'chat_%s' % self.room_name
        
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name
        )
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        userID = text_data_json["userID"]
        room_name = text_data_json["room_name"]
        
        await self.save_message(message, userID, room_name)     

        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
                "userID": userID,
                "room_name": room_name,
            }
        )
        
    async def sendMessage(self, event):
        message = event["message"]
        userID = event["userID"]
        await self.send(text_data=json.dumps({"message": message, "userID": userID}))
    
    @sync_to_async
    def save_message(self, message, userID, room_name):
        print(userID,room_name,"----------------------")
        user=User.objects.get(userID=userID)
        room=Room.objects.get(name=room_name)
        
        ChatMessage.objects.create(user=user,room=room,content=message)