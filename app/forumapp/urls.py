from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from forumapp import views

router = DefaultRouter()
router.register('posts', views.PostsViewSet)

urlpatterns = [
    # JWT endpoints
    path('login/', TokenObtainPairView.as_view(), name='jwt_login'),
    path('refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),

    # Register endpoint
    path('register/', views.RegisterApiView.as_view(), name='register'),

    # Dashboard endpoints
    path('dashboard/', views.DashboardView.as_view(), name='user-profile'),
    path('dashboard/my_posts/', views.DashboardAllPostsView.as_view(), name='all-posts'),
    path('dashboard/liked_posts/', views.DashboardLikedByMePosts.as_view(),name='liked-posts'),

    # Posts endpoints
    path('', include(router.urls)),
]
