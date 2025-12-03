from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from forumapp import serializers, models
from forumapp.permissions import IsNotAuthenticated
from forumapp.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication

User = get_user_model()


# Posts API
class PostsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = serializers.PostsDetailSerializer
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

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PostsSerializer
        return self.serializer_class


# Register API
class RegisterApiView(generics.CreateAPIView):
    serializer_class = serializers.RegisterUserSerializer
    permission_classes = [IsNotAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)


# Dashboard API
class DashboardView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.DashboardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class DashboardAllPostsView(generics.RetrieveAPIView):
    serializer_class = serializers.DashboardAllPostsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class DashboardLikedByMePosts(generics.ListAPIView):
    serializer_class = serializers.PostsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return models.Posts.objects.filter(likes=user).order_by('-posted_on')


# User Profile API
# Go to every user profile and check their posts and info
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = serializers.PublicUserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    lookup_field = "pk"

# Comments to posts API
class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentsSerializer
    queryset = models.Comments.objects.all()
    permission_classes = [permissions.IsAuthenticated,]
    authentication_classes = [JWTAuthentication,]

    def perform_create(self,serializer):
        serializer.save(commentor=self.request.user)