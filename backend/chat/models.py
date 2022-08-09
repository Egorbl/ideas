from django.db import models
from authentication.models import Account


class Chat(models.Model):
    id = models.UUIDField(unique=True, primary_key=True)
    owner = models.ForeignKey(to=Account, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    participants = models.ManyToManyField(
        to=Account, related_name="chats", blank=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    id = models.UUIDField(unique=True, primary_key=True)
    owner = models.ForeignKey(to=Account, on_delete=models.PROTECT)
    chat = models.ForeignKey(
        to=Chat, related_name="messages", on_delete=models.CASCADE)
    content = models.TextField(max_length=10000)
    date_added = models.DateTimeField(auto_now_add=True)
