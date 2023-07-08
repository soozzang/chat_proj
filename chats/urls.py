from django.urls import path
from .views import *
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()

app_name = 'chats'

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version="v1",
        description="Your API description",
    ),
    public=True,
)

urlpatterns = [
    path("",index,name="index"),
    path("room/<int:pk>/", RoomDetail.as_view(), name="room_detail_destroy"),
    
    path("room_list_create/", RoomList.as_view(), name="room_list_create"),
    
    path("room/<int:room_id>/chat_list/", ChatList.as_view(), name="chat_list"),

    #세부기능

    path('room/<int:room_id>/enter/',Users_in_room.as_view(), name='users_in_room'),

    path('room/<int:room_id>/exit/',ExitRoom.as_view(), name = 'exit_room'),



    #회원관련

    path('signup/', Signup.as_view()),

    path('login/', Login.as_view()),

    path('logout/', Logout.as_view()),

    path('myinfo/', MyInfo.as_view()),

    #swagger
    
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),


]