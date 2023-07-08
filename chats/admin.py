from django.contrib import admin
from .models import Room,ChatMessage,User
# Register your models here.

admin.site.register(Room)
admin.site.register(ChatMessage)
admin.site.register(User)