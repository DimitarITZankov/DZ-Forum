from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            return Response({'status': 'unliked', 'total_likes': post.total_likes()}, status=status.HTTP_200_OK)
        else:
            post.likes.add(user)
            return Response({'status': 'liked', 'total_likes': post.total_likes()}, status=status.HTTP_200_OK)


# Register API
class RegisterApiView(generics.CreateAPIView):
    serializer_class = serializers.RegisterUserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)


# Profile API

class DashboardAllPostsView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.DashboardAllPostsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Return the currently logged-in user
        return self.request.user