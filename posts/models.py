from django.utils import timezone
from django.db import models
from django.contrib.contenttypes.fields import ContentType, GenericForeignKey, GenericRelation
from django.utils.text import slugify
from django.dispatch import Signal
from drf_chunked_upload.models import ChunkedUpload
from django.contrib.auth import get_user_model
from django.db import models

from users.models import CustomeUserModel
from datetime import datetime, timedelta



TAG_CHOICE = {
    ('Programming', 'Programming'),
    ('Science', 'Scince')
}

def get_podcast_filepath(self, filename):
    title = slugify(self.title)
    return f'post/podcast/{title}.mp3'


def get_post_image_filepath(self, filename):
    return f'post/image/{self.title[0:15] + ".png"}'

def get_default_post_image():
    return "default_image.jpg" 

"""
    create custom update singal
    whenever objects updated if user is not admin the admin-check = False

"""
post_update = Signal()

class MyCustomQuerySet(models.query.QuerySet):
    def update(self, kwargs):
        super(MyCustomQuerySet, self).update(kwargs)
        post_update.send(sender=self.model)

class MyCustomManager(models.Manager):
    def getqueryset(self):
        return MyCustomQuerySet(self.model, using=self._db)

class Comment(models.Model):
    class Meta:
        ordering = ['created_time']

    content_type= models.ForeignKey(ContentType,
                    limit_choices_to = {
                        'model__in':('post', 'podcast', 'successfullexperience')
                        }, on_delete=models.CASCADE)
    object_id   = models.PositiveIntegerField()
    item        = GenericForeignKey('content_type', 'object_id')
    owner       = models.ForeignKey(CustomeUserModel, on_delete=models.RESTRICT, null=False, blank=False)
    comment_text= models.TextField(max_length=100, blank=True, null=True)
    user_liked  = models.ManyToManyField(CustomeUserModel, related_name="comment_liked", blank=True)
    created_time= models.DateTimeField(auto_now_add = True)
    updated_time= models.DateTimeField(auto_now = True)
    admin_check = models.BooleanField(default=False)
    
    @property
    def short_comment_text(self):
        return f'{self.comment_text[0:15]}...'

class Demand(models.Model):
    owner         = models.ForeignKey(CustomeUserModel, on_delete=models.CASCADE)
    suggested_money = models.DecimalField(default=0, decimal_places=4, max_digits=12)
    suggested_time= models.DateTimeField(blank=True, auto_now=False, auto_now_add=False)  
    def __str__(self):
        return f'{self.owner} suggested time = {self.suggested_time}'
   

class ItemBase(models.Model):
    owner        = models.ForeignKey(CustomeUserModel, related_name="%(class)s_related", on_delete=models.CASCADE)
    title        = models.CharField(max_length = 250)
    description  = models.TextField()
    created_time = models.DateTimeField(auto_now_add = True)
    updated_time = models.DateTimeField(auto_now = True)
    admin_check  = models.BooleanField(default=False)
    user_liked   = models.ManyToManyField(CustomeUserModel, related_name="%(class)s_liked", blank=True)
    user_saved   = models.ManyToManyField(CustomeUserModel, related_name="%(class)s_saved", blank=True)
    # objects     = MyCustomManager()
    class Meta:
        abstract = True

    @property
    def short_title(self):
        if len(self.title) > 16:
            return f'{self.title[0:15]}...'
        return self.title 

    def __str__(self):
        return self.short_title

class Post(ItemBase):
    image       = models.ImageField(max_length=255, upload_to=get_post_image_filepath, null=True, blank=True, default=get_default_post_image)
    comment     = GenericRelation(Comment)
    
class Podcast(ItemBase):
    file         = models.FileField(upload_to=get_podcast_filepath)
    comment     = GenericRelation(Comment)

class Project(ItemBase):
    user_accepted   = models.ForeignKey(CustomeUserModel, related_name="project_accepted", null=True, blank=True, on_delete=models.SET_NULL)
    demands         = models.ManyToManyField(Demand, related_name="project", blank=True)
    preferred_time  = models.DateTimeField()
    money_min       = models.DecimalField(decimal_places=4, max_digits=12)
    money_max       = models.DecimalField(decimal_places=4, max_digits=12)
    designated_money= models.DecimalField(blank=True, null=True,  decimal_places=4, max_digits=12) 
    designated_time = models.DateTimeField(blank=True, null=True)
    finished        = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.id}-{self.owner} project'
 
class HoldProjectMoney(models.Model):
    sender      = models.ForeignKey(CustomeUserModel, related_name="sender_project_money", on_delete=models.CASCADE)
    receiver    = models.ForeignKey(CustomeUserModel, related_name="receiver_project_money", on_delete=models.CASCADE)
    project     = models.OneToOneField(Project, on_delete=models.CASCADE)
    amount      = models.DecimalField(blank=False, decimal_places=4, max_digits=12)

class SuccessfullExperience(ItemBase):
    user_liked   = models.ManyToManyField(CustomeUserModel, related_name="exprience_liked", blank=True)
    user_saved   = models.ManyToManyField(CustomeUserModel, related_name="exprience_saved", blank=True)
    comment     = GenericRelation(Comment)
    @property
    def day_pass(self):
        return timezone.now() - self.created_time


class MoneyUnit(models.Model):
    like_money   = models.DecimalField(default=0.01, decimal_places=4, max_digits=12)
    podcast_money= models.DecimalField(default=0.01, decimal_places=4, max_digits=12)
    comment_money= models.DecimalField(default=0.01, decimal_places=4, max_digits=12)

    
# class UploadType(ChunkedUpload):
#     ALLOWED_CONTENT_TYPES = [User]
#     MIN_BYTES = 0
#     MAX_BYTES = 50 * 1024 * 1024
#     ALLOWED_EXTENSIONS = None
#     ALLOWED_MIMETYPES = ['video/mp4']

#     file = models.FileField(
#         max_length=255,        null=True)

#     def allowed_owners(self):
#         return super(UploadType, self).allowed_owners()

#     def allowed_owner(self, owner_type, owner_id=None, msg=None):
#         return super(UploadType, self).allowed_owner(owner_type, owner_id, msg)



#     product         = models.ForeignKey(Product, related_name='products',
#                         on_delete=models.CASCADE, blank=False)
#     comment_parent  = models.ForeignKey('ProductComment', null=True, blank=True,
#                         on_delete=models.CASCADE)
#     
#     
#     like_count      = models.PositiveIntegerField(default=0, null=True, blank=True)
#     dislike_count   = models.PositiveIntegerField(default=0, null=True, blank=True)

