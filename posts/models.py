from django.db import models

from users.models import CustomeUserModel

TAG_CHOICE = {
    ('Programming', 'Programming'),
    ('Science', 'Scince')
}

def get_post_image_filepath(self, filename):
    return f'post/image/{self.title[0:15] + ".png"}'

def get_default_post_image():
    return "post/image/default_post_image.png" 


# class PostTag(models.Model):
#     title        = models.CharField(max_length = 40, blank=True)

class ItemBase(models.Model):
    owner        = models.ForeignKey(CustomeUserModel, related_name="%(class)s_related", on_delete=models.CASCADE)
    title        = models.CharField(max_length = 250)
    description  = models.TextField()
    created_time = models.DateTimeField(auto_now_add = True)
    updated_time = models.DateTimeField(auto_now = True)
    user_saved   = models.ForeignKey(CustomeUserModel, related_name="%(class)s_saved", blank=True, null=True, on_delete=models.CASCADE)
    user_liked   = models.ForeignKey(CustomeUserModel, related_name="%(class)s_liked", blank=True, null=True, on_delete=models.CASCADE)


class Post(ItemBase):
    image        = models.ImageField(max_length=255, upload_to=get_post_image_filepath, null=True, blank=True, default=get_default_post_image)

class Podcast(ItemBase):
    file         = models.FileField( upload_to=get_post_image_filepath, null=True, blank=True, default=get_default_post_image)
  



# class Comment(models.Model):
#     product         = models.ForeignKey(Product, related_name='products',
#                         on_delete=models.CASCADE, blank=False)
#     comment_parent  = models.ForeignKey('ProductComment', null=True, blank=True,
#                         on_delete=models.CASCADE)
#     user            = models.ForeignKey(CustomUser, on_delete=models.RESTRICT, null=False, blank=False)
#     comment_text    = models.TextField(max_length=100, blank=True, null=True)
#     like_count      = models.PositiveIntegerField(default=0, null=True, blank=True)
#     dislike_count   = models.PositiveIntegerField(default=0, null=True, blank=True)

