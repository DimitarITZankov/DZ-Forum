from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.response import Response
from forumapp import serializers, models
from forumapp.permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
from django.shortcuts import render

User = get_user_model()


# Posts API
class PostsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = serializers.PostsSerializer
    queryset = models.Posts.objects.order_by('-posted_on')
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['category', 'title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# Register API
class RegisterApiView(generics.CreateAPIView):
    serializer_class = serializers.RegisterUserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
