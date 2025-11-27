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

User = get_user_model()

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password']  # adjust 'name' if using custom user

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data.get('name', ''),
            password=validated_data['password']
        )
        return user