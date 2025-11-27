from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from forumapp import serializers,models
from forumapp.permissions import IsOwnerOrReadOnly

class PostsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,IsOwnerOrReadOnly]
    serializer_class = serializers.PostsSerializer
    queryset = models.Posts.objects.all()
    def perform_create(self,serializer):
    	serializer.save(author=self.request.user)

