from django.contrib import admin
from .models import Room,ChatMessage,Profile
# Register your models here.

admin.site.register(Room)
admin.site.register(ChatMessage)
admin.site.register(Profile)