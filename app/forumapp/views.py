from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from forumapp import serializers,models
from forumapp.permissions import IsOwnerOrReadOnly

class PostsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,IsOwnerOrReadOnly]
    serializer_class = serializers.PostsSerializer
    queryset = models.Posts.objects.order_by('-posted_on')
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['category', 'title', 'content']  # Allows filtering by category
    def perform_create(self,serializer):
    	serializer.save(author=self.request.user)

