from django.http import JsonResponse
from django.shortcuts import render,redirect
from rest_framework import generics
from django.contrib import auth
from chats.serializers import RoomSerializer,ChatMessageSerializer,UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Room,ChatMessage,User
from drf_yasg.utils import swagger_auto_schema




def index(request):
    return render(request,'index.html')
#회원 
class Signup(APIView):
    serializer_class = UserSerializer

    @swagger_auto_schema(
        responses={200: UserSerializer()},
        tags=["User"]
    )


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Success Signup!", "user": serializer.data}, status=200)


    
class Login(APIView):
    def post(self, request):
        userID = request.data["userID"]
        password = request.data["password"]

        user = auth.authenticate(userID = userID, password = password)

        if user is not None:
            auth.login(request, user)
            return Response({"id": user.id}, status = 200)
        else:
            return Response({"message": "유저 정보가 없습니다"}, status = 403)

class Logout(APIView):
    def get(self, request):
        if request.user is not None: 
            auth.logout(request)
            return Response(status=200)
        else:
            return Response(status=403)
        
class MyInfo(APIView):
    def get(self, request):
        user = request.user

        if user is not None:
            rooms = user.get_user_rooms()
            room_names = [room.name for room in rooms]
            serializer = UserSerializer(user)
            return JsonResponse({"user": serializer.data, "rooms": room_names})
        else:
            return Response({"message": "로그아웃 상태입니다."})
        


#채팅방 CRUD

class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all().order_by("-id")
    serializer_class = RoomSerializer

class RoomDetail(generics.RetrieveDestroyAPIView):
    queryset = Room.objects.all().order_by("-id")
    serializer_class = RoomSerializer
    lookup_field = 'pk'

#채팅기록 Read

class ChatList(generics.ListAPIView):
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        return ChatMessage.objects.filter(room_id=room_id).order_by("-id")
    

#!부가기능!

# 총 조회수와, 속한 인원수 파악하는 기능/user가 처음 방에 들어갈 때는 user_count와 entry_count에 +=1 / 이미 들어간 user면, entry_count만 +=1 하게 끔 만듬.
class Users_in_room(APIView):
    def post(self, request, room_id):
        user=request.user
        room = Room.objects.get(id=room_id)
        if user not in room.user.all():
            room.user.add(user)
            room.user_count+=1
            room.entry_count+=1
            room.save()
        else:
            room.entry_count+=1
            room.save()
        return Response({"message": "방에 입장되었습니다","user_count":room.user_count,"entry_count":room.entry_count})
#방 나가기 기능.

class ExitRoom(APIView):
    def post(self, request, room_id):
        user = request.user
        room = Room.objects.get(id=room_id)
        if user in room.user.all():
            room.user.remove(user)
            room.user_count -= 1
            room.save()
        return Response({"message": "방에서 나왔습니다","user_count":room.user_count,"entry_count":room.entry_count})
    











