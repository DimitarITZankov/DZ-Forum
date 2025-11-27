from rest_framework import serializers
from forumapp import models

class PostsSerializer(serializers.ModelSerializer):
    # Show the author under posts by its name instead of the ID
    author = serializers.SerializerMethodField()

    class Meta:
        model = models.Posts
        fields = ['id', 'title', 'author', 'content', 'posted_on']
        extra_kwargs = {'posted_on': {'read_only': True}}

    def get_author(self, obj):
        return obj.author.name or obj.author.email