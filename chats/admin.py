from django.contrib import admin
from .models import Room,ChatMessage,User,Category
# Register your models here.

admin.site.register(Room)
admin.site.register(ChatMessage)
admin.site.register(User)
admin.site.register(Category)