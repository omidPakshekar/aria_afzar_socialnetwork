from django.contrib import admin

from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'short_title', 'created_time']

class ExprienceAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'title', 'created_time', 'day_pass', 'admin_check']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'short_comment_text',
             'created_time', 'content_type', 'item', 'admin_check']


admin.site.register(Podcast, PostAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(SuccessfullExperience, ExprienceAdmin)
admin.site.register(Comment, CommentAdmin)


