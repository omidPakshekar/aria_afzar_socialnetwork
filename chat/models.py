from cgitb import text
from pyexpat import model
from django.db import models
from users.models import CustomeUserModel

class Contact(models.Model):
    owner       = models.ForeignKey(CustomeUserModel, related_name='contacts', on_delete=models.CASCADE)
    friends     = models.ManyToManyField(CustomeUserModel, blank=True)

    def __str__(self):
        return self.owner.username
    
    @property
    def list_5_first_friends(self):
        frinds =  self.friends.all()[0:5]
        return ' '.join([str(i) for i in frinds])

class Message(models.Model):
    owner          = models.ForeignKey(CustomeUserModel, related_name='chat_messages', on_delete=models.CASCADE)
    parent_message = models.OneToOneField('Message', related_name='child', null=True,
                          on_delete=models.SET_NULL, blank=True)
    message_text   = models.TextField()
    timestamp      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact.owner.username

class Chat(models.Model):
    participants = models.ForeignKey(Contact, related_name='chats', blank=True, on_delete=models.CASCADE)
    messages     = models.ManyToManyField(Message, blank=True)

    def last_10_messages(self):
        return self.messages.objects.order_by('-timestamp')
    def __str__(self):
        return "{}".format(self.pk)



