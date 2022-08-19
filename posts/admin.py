from django.contrib import admin

from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'short_title', 'created_time']

class ExprienceAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_time', 'admin_check']



admin.site.register(Podcast, PostAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(SuccessfullExperience, ExprienceAdmin)


