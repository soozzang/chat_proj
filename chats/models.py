from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(str(self.id))
        super().save(*args, **kwargs)

    
class Profile(AbstractUser):
    created_rooms = models.ManyToManyField(Room, related_name='created_by',blank=True)
    fixed_rooms = models.ManyToManyField(Room, related_name='fixed_for', blank=True)

    def __str__(self):
        return str(self.username)
    
class ChatMessage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    nick = models.CharField(max_length=15)
    content = models.TextField()

    def __str__(self):
        return f"{self.room.name}-{self.nick}"
    
    def get_chat_id(self):
        return self.room_id