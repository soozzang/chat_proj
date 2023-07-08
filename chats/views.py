from django.shortcuts import render,redirect
from .forms import RoomForm
from rest_framework.decorators import api_view
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from .models import Room,ChatMessage

#회원 

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('chats:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form' : form})

#메인 페이지

def index(requset):
    return render(requset,'index.html')

#방 생성

def room_create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save()
            return redirect('chats:room_list')
    else:
        form = RoomForm()
    
    context = {
        'form': form
    }
    return render(request, 'room_create.html', context)

#채팅방

def room_chat(request, slug):
    room_name=Room.objects.get(slug=slug).name
    messages=ChatMessage.objects.filter(room=Room.objects.get(slug=slug))

    context = {
        'room_name' : room_name,
        'slug' : slug,
        'messages': messages,
    }
    return render(request, 'room_chat.html', context)

#채팅방 목록

def room_list(request):
    rooms = Room.objects.all()

    context = {
        'rooms': rooms,
    }

    return render(request, 'room_list.html', context)

#마이페이지

def mypage(request):
    pass

#검색페이지

def search(request):
    return render(request, 'search.html')









