from django.db import models
from users.models import CustomeUserModel

class Contact(models.Model):
    owner = models.ForeignKey(CustomeUserModel, related_name='friends', on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username

class Message(models.Model):
    owner = models.ForeignKey(CustomeUserModel, related_name='chat_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_10_messages():
        return Message.objects.order_by('-timestamp').all()[:10]

class Chat(models.Model):
    participants = models.ManyToManyField(Contact, related_name='chats', blank=True)
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return "{}".format(self.pk)



