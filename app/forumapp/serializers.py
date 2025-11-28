from rest_framework import serializers
from forumapp import models
from django.contrib.auth import get_user_model

class PostsSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()

    class Meta:
        model = models.Posts
        fields = ['id', 'title', 'author', 'content', 'posted_on', 'category', 'total_likes']

    def get_author(self, obj):
        return obj.author.name or obj.author.email

    def get_total_likes(self, obj):
        return obj.total_likes()

# Return my custom user model 
User = get_user_model()

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data.get('name', ''),
            password=validated_data['password']
        )
        return user


class DashboardSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['email', 'name', 'password']
        read_only_fields = ['email']  # Email cannot be changed

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class DashboardAllPostsSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['posts']

    def get_posts(self, obj):
        return PostsSerializer(obj.posts_set.all(), many=True).data