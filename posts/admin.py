from django.contrib import admin

from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'short_title', 'created_time']



admin.site.register(Podcast, PostAdmin)
admin.site.register(Post, PostAdmin)


