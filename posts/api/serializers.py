from rest_framework import serializers

from users.models import CustomeUserModel

from ..models import Comment, Podcast, Post, SuccessfullExperience
from payment.api.serializers import UserInlineSerializer

class CommentInlineSerializer(serializers.ModelSerializer):
    comment_likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'owner', 'comment_text', 'comment_likes']

    def get_comment_likes(self, obj):
        return obj.user_liked.count()

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
    owner = UserInlineSerializer(read_only=True)
    comment = CommentInlineSerializer(many=True ,read_only = True)
    class Meta:
        model = SuccessfullExperience
        fields = ['id','owner', 'title', 'description', 'likes', 'save_number', 'comment']

    def get_likes(self, obj):
        return obj.user_liked.count()

    def get_save_number(self, obj):
        return obj.user_saved.count()

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
    owner = UserInlineSerializer(read_only=True)
    comment = CommentInlineSerializer(many=True ,read_only = True)

    class Meta:
        model = Post
        fields = ['id','owner', 'image', 'title', 'description', 'likes', 'save_number', 'comment']

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


"""
    podcast serializer
"""

class PodcastCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = ['file', 'title', 'description']
    
    def validate_file(self, value):
        if 'mp3' not in value._name:
            raise serializers.ValidationError("file must be mp3.")
        return value

class PodcastUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = ['id','title', 'description', 'file']

class PodcastAdminUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = ['id','title', 'description','file', 'admin_check']

class PodcastSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    save_number = serializers.SerializerMethodField(read_only=True)
    owner = UserInlineSerializer(read_only=True)
    comment = CommentInlineSerializer(many=True ,read_only = True)
    class Meta:
        model = Podcast
        fields = ['id','owner', 'file', 'title', 'description', 'likes', 'save_number', 'comment']

    def get_likes(self, obj):
        return obj.user_liked.count()

    def get_save_number(self, obj):
        return obj.user_saved.count()
    
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment_text']
