from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)


class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000000)
    timestamp = models.DateTimeField(auto_now=True)

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender,
            "content": self.content,
            "timestamp": self.timestamp,
        }

    def __str__(self):
        return f"<Post id:{self.id} sender: {self.sender}>"