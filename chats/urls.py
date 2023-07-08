from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views


app_name = 'chats'

urlpatterns = [
    path('', index, name="index"),
    
    path('room_chat/<str:slug>/', room_chat, name='room_chat'),
    
    path('room_create/', room_create, name='room_create'),
    
    path('room_list/', room_list, name='room_list'),

    path('mypage/', mypage, name='mypage'),

    path('search/', search, name='search'),

    #회원관련

    path('signup/', signup, name='signup'),

    path('login/', LoginView.as_view(template_name='login.html'), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),



]