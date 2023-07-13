from django.shortcuts import render,redirect
from rest_framework import generics
from django.contrib import auth
from chats.serializers import RoomSerializer,ChatMessageSerializer,UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Room,ChatMessage,User
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


def index(request):
    return render(request,'index.html')
#회원 
class Signup(APIView):

    @swagger_auto_schema(
        responses={200: UserSerializer()},
        tags=["User"]
    )


    def post(self, request):
        user_id = request.data.get("userID")
        password = request.data.get("password")

        if not user_id or not password:
            return Response({"message": "공백이 존재합니다"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(userID=user_id)
            return Response({"message": "해당 ID를 가진 유저가 이미 존재합니다."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            user = User.objects.create_user(userID=user_id, password=password)
            return Response({"message": "회원가입이 완료되었습니다!", "userID": user.userID}, status=status.HTTP_200_OK)


    
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
            return Response({"message":"비로그인 상태입니다."},status=403)


class UserInfo(APIView):
    def get(self, request,id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"message": "해당 사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        rooms = user.get_user_rooms()
        room_names = [room.name for room in rooms]
        return Response({"user": user.id, "userID": user.userID, "rooms": room_names})
    
class MyInfo(APIView):
    def get(self, request):
        try:
            user = request.user
        except User.DoesNotExist:
            return Response({"message": "로그인 해주세요."}, status=status.HTTP_404_NOT_FOUND)

        rooms = user.get_user_rooms()
        room_names = [room.name for room in rooms]
        return Response({"user": user.id, "userID": user.userID, "rooms": room_names})


#채팅방 CRUD

class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all().order_by("-id")
    serializer_class = RoomSerializer

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated: 
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "로그인 하세요."}, status=status.HTTP_401_UNAUTHORIZED)


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
        return Response({"message": "방에 입장되었습니다","room_name": room.name,"user_count":room.user_count,"entry_count":room.entry_count})
#방 나가기 기능.

class ExitRoom(APIView):
    def post(self, request, room_id):
        user = request.user
        room = Room.objects.get(id=room_id)
        if user in room.user.all():
            room.user.remove(user)
            room.user_count -= 1
            room.save()
        return Response({"message": "방에서 나왔습니다","room_name": room.name,"user_count":room.user_count,"entry_count":room.entry_count})
    



def room_chat(request, name):
    messages=ChatMessage.objects.filter(room=Room.objects.get(name=name))

    context = {
        'room_name' : name,
        'messages': messages,
        'room_name' : name,
    }
    return render(request, 'room_chat.html', context)
    









