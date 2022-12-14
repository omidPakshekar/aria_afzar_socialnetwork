from dataclasses import field, fields
from rest_framework import serializers

from users.models import CustomeUserModel

from ..models import Comment, Demand, MoneyUnit, Podcast, Post, Project, SuccessfullExperience
from users.api.serializers import UserIdInlineSerializer, UserInlineSerializer, UserInlineSerializerNonAdmin


class IdSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

"""
    comment serializer
"""
class CommentInlineSerializer(serializers.ModelSerializer):
    comment_likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'owner', 'parent_id', 'comment_text', 'comment_likes']

    def get_comment_likes(self, obj):
        return obj.user_liked.count()

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment_text', 'parent_id']
class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id"]
"""
    project serializer
"""
class DemandListSerializer(serializers.ModelSerializer):
    owner = UserInlineSerializerNonAdmin(read_only=True)
    class Meta:
        model = Demand
        fields = "__all__"
class DemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demand
        fields= ["suggested_time", "suggested_money"]
class DemandIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    
class ProjectSerializer(serializers.ModelSerializer):
    owner = UserInlineSerializerNonAdmin(read_only=True)
    user_accepted = UserInlineSerializerNonAdmin(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    save_number = serializers.SerializerMethodField(read_only=True)
    request_number = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Project
        exclude = ['demands', 'user_liked', 'user_saved', 'updated_time'] 
   
    def get_likes(self, obj):
        return obj.user_liked.count()
    def get_save_number(self, obj):
        return obj.user_saved.count()  
    def get_request_number(self, obj):
        return obj.demands.count()

class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project 
        fields = ['title', 'description', 'money_max', 'money_min', 'preferred_time']

class ProjectAdminUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project 
        fields = ['title', 'description', 'money_max', 'money_min', 'preferred_time', 'admin_check']

class ProjectListSerializer(serializers.ModelSerializer):
    # demands = DemandSerializer(many=True)
    class Meta:
        model = Project 
        # fields = "__all__"
        exclude = ['demands'] 

class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project 
        fields = ["title", "description", "money_min", "money_max", "preferred_time"]

class ProjectAdminCheckSerializer(serializers.ModelSerializer):
    owner = UserInlineSerializerNonAdmin(read_only=True)
    class Meta:
        model = Podcast
        fields = ['id','owner', 'file', 'title', 'description', 'admin_check']

"""
    succefullexprience serializer
"""
class ExprienceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessfullExperience
        fields = ['title', 'description']

class ExprienceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessfullExperience
        fields = ['id','title', 'description']

class ExprienceAdminUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessfullExperience
        fields = ['id','title', 'description', 'admin_check']

class ExprienceSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    save_number = serializers.SerializerMethodField(read_only=True)
    owner = UserInlineSerializerNonAdmin(read_only=True)
    # comment = CommentInlineSerializer(many=True ,read_only = True)
    class Meta:
        model = SuccessfullExperience
        fields = ['id','owner', 'title', 'description', 'likes', 'save_number',]

    def get_likes(self, obj):
        return obj.user_liked.count()

    def get_save_number(self, obj):
        return obj.user_saved.count()

class ExprienceAdminCheckSerializer(serializers.ModelSerializer):
    owner = UserInlineSerializer(read_only=True)
    class Meta:
        model = SuccessfullExperience
        fields = ['id','owner', 'title', 'description', 'admin_check']


# class ExprienceChangeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SuccessfullExperience
#         fields = 

"""
    post serializer
"""
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['image', 'title', 'description']

class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    save_number = serializers.SerializerMethodField(read_only=True)
    owner = UserInlineSerializerNonAdmin(read_only=True)
    class Meta:
        model = Post
        fields = ['id','owner', 'image', 'title', 'description', 'likes', 'save_number', 'created_time']

    def get_likes(self, obj):
        return obj.user_liked.count()

    def get_save_number(self, obj):
        return obj.user_saved.count()

class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title', 'description', 'image']

class PostAdminUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title', 'description', 'image' ,'admin_check']

class PostAdminCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title', 'description', 'image' ,'admin_check']

"""
    podcast serializer
"""

class PodcastCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = ['file', 'title', 'cover', 'description']
    
    def validate_file(self, value):
        if 'mp3' not in value._name:
            raise serializers.ValidationError("file must be mp3.")
        return value

class PodcastUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = ['id','title', 'cover', 'description', 'file']

class PodcastAdminUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = ['id','title', 'cover', 'description','file', 'admin_check']

class PodcastSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    save_number = serializers.SerializerMethodField(read_only=True)
    owner = UserInlineSerializerNonAdmin(read_only=True)
    comment = CommentInlineSerializer(many=True ,read_only = True)
    class Meta: 
        model = Podcast
        fields = ['id','owner', 'cover', 'file', 'title', 'description', 'likes', 'save_number', 'comment']

    def get_likes(self, obj):
        return obj.user_liked.count()

    def get_save_number(self, obj):
        return obj.user_saved.count()
    
class PodcastAdminCheckSerializer(serializers.ModelSerializer):
    owner = UserInlineSerializerNonAdmin(read_only=True)
    class Meta:
        model = Podcast
        fields = ['id','owner', 'file', 'cover', 'title', 'description', 'admin_check']

"""
    MoneyUnit
"""
class MoneyUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyUnit
        fields = "__all__"






