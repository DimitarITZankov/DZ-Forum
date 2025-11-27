from rest_framework import serializers
from forumapp import models
from django.contrib.auth import get_user_model

class PostsSerializer(serializers.ModelSerializer):
    # Show the author under posts by its name or email instead of the ID
    author = serializers.SerializerMethodField()

    class Meta:
        model = models.Posts
        fields = ['title', 'author', 'content', 'posted_on','category'] # Dont show the ID in the /posts/ endpoint
        extra_kwargs = {'posted_on': {'read_only': True}}

    # Get the author name or email instead of the ID
    def get_author(self, obj):
        return obj.author.name or obj.author.email

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