from django.contrib import admin

from .models import *

class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'list_5_first_friends']

class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'message_text', 'parent_message', 'timestamp']

class ChatAdmin(admin.ModelAdmin):
    list_display = ['id',]



admin.site.register(Message, MessageAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(Contact, ContactAdmin)



