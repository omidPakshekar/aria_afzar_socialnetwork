from django.contrib import admin
from drf_chunked_upload.models import ChunkedUpload 

from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'short_title', 'created_time']

class ExprienceAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'title', 'created_time', 'day_pass', 'admin_check']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'short_comment_text',
             'created_time', 'content_type', 'item', 'admin_check']

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['owner',  'user_accepted', 'designated_money', 'finished', 'designated_money']

class HoldProjectMoneyAdmin(admin.ModelAdmin):
    list_display = ['sender',  'receiver', 'amount', 'project']

admin.site.register(Podcast, PostAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(SuccessfullExperience, ExprienceAdmin)
admin.site.register(Comment, CommentAdmin)
# admin.site.register(Project, ProjectAdmin)
# admin.site.register(HoldProjectMoney, HoldProjectMoneyAdmin)
admin.site.register(Demand)
admin.site.register(MoneyUnit)
