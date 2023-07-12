from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManger(BaseUserManager):
    use_in_migrations = True

    def create_user(self, userID, password):

        user = self.model(
            userID = userID
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, userID, password):
        superuser = self.create_user(userID = userID, password = password)
        superuser.is_staff_user = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        
        return superuser
    
class User(AbstractBaseUser, PermissionsMixin):
    userID = models.CharField(max_length=50, unique = True)
    is_active = models.BooleanField(default=True)
    is_staff_user = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    
    def is_staff(self):
        return self.is_staff_user

    def get_user_rooms(self):
        return Room.objects.filter(user=self)

    
    objects = UserManger()

    USERNAME_FIELD = 'userID'

    class Meta:
        db_table = 'user'

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Room(models.Model):
    user = models.ManyToManyField(User, related_name="room_users")
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='room_images/',null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user_count = models.PositiveIntegerField(default=0)
    entry_count = models.PositiveIntegerField(default=0)
    password = models.CharField(max_length=100, null=True, blank=True)
    is_public =  models.BooleanField(default=True)
    def __str__(self):
        return str(self.name)
    


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()

    def __str__(self):
        return f"{self.room.name}-{self.user}"
    