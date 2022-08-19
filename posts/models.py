from django.db import models

from users.models import CustomeUserModel
from datetime import datetime, timedelta


TAG_CHOICE = {
    ('Programming', 'Programming'),
    ('Science', 'Scince')
}

def get_post_image_filepath(self, filename):
    return f'post/image/{self.title[0:15] + ".png"}'

def get_default_post_image():
    return "default_image.jpg" 


# class PostTag(models.Model):
#     title        = models.CharField(max_length = 40, blank=True)

class ItemBase(models.Model):
    owner        = models.ForeignKey(CustomeUserModel, related_name="%(class)s_related", on_delete=models.CASCADE)
    title        = models.CharField(max_length = 250)
    description  = models.TextField()
    created_time = models.DateTimeField(auto_now_add = True)
    updated_time = models.DateTimeField(auto_now = True)
    admin_check  = models.BooleanField(default=False)

    @property
    def short_title(self):
        if len(self.title) > 16:
            return f'{self.title[0:15]}...'
        return self.title 

    def __str__(self):
        return self.short_title

class Post(ItemBase):
    image        = models.ImageField(max_length=255, upload_to=get_post_image_filepath, null=True, blank=True, default=get_default_post_image)
    user_liked   = models.ManyToManyField(CustomeUserModel, related_name="posts_liked", blank=True)
    user_saved   = models.ManyToManyField(CustomeUserModel, related_name="posts_saved", blank=True)

class Podcast(ItemBase):
    file         = models.FileField( upload_to=get_post_image_filepath, null=True, blank=True, default=get_default_post_image)
    user_liked   = models.ManyToManyField(CustomeUserModel, related_name="podcasts_liked", blank=True)
    user_saved   = models.ManyToManyField(CustomeUserModel, related_name="podcasts_saved", blank=True)

class SuccessfullExperience(ItemBase):
    user_liked   = models.ManyToManyField(CustomeUserModel, related_name="exprience_liked", blank=True)
    user_saved   = models.ManyToManyField(CustomeUserModel, related_name="exprience_saved", blank=True)



# class Comment(models.Model):
#     product         = models.ForeignKey(Product, related_name='products',
#                         on_delete=models.CASCADE, blank=False)
#     comment_parent  = models.ForeignKey('ProductComment', null=True, blank=True,
#                         on_delete=models.CASCADE)
#     user            = models.ForeignKey(CustomUser, on_delete=models.RESTRICT, null=False, blank=False)
#     comment_text    = models.TextField(max_length=100, blank=True, null=True)
#     like_count      = models.PositiveIntegerField(default=0, null=True, blank=True)
#     dislike_count   = models.PositiveIntegerField(default=0, null=True, blank=True)

