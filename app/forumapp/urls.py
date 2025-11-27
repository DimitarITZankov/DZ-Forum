from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,) 
from forumapp import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('posts', views.PostsViewSet)


urlpatterns = [
	path('login/', TokenObtainPairView.as_view(),name='jwt_login'),
	path('refresh/', TokenRefreshView.as_view(),name='jwt_refresh'),
	path('', include(router.urls)),

]