from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,PermissionsMixin,BaseUserManager,)
from django.conf import settings

class UserManager(BaseUserManager):
	#Manager for users
	def create_user(self,email,password=None,**extra_fields): #The **extra_fields here are provoding all the non-must fields to our model, 
															 #so whenever we add a new field to our model, we dont need to pass it
		if not email:
			raise ValueError('User must have an email address')
		user = self.model(email=self.normalize_email(email),**extra_fields) #we normalize the email directly when we create the user instead of creating a variable and then assing it
		user.set_password(password)
		user.save(using=self._db) #This supports adding multiple databases to one project
		return user

	def create_superuser(self,email,password):
		#Creating superuser using the django CLI
		user = self.create_user(email,password)
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

class User(AbstractBaseUser,PermissionsMixin):
	# Creating custom user model
	email = models.EmailField(max_length=255,unique=True)
	name = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	objects = UserManager() #We assign our model to the custom user manager

	# Assign the login field and the required fields for creating users
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name']

	def __str__(self):
		return self.name


class Posts(models.Model):
    CATEGORY_CHOICES = [
        ('TECH', 'Tech'),
        ('LIFE', 'Lifestyle'),
        ('NEWS', 'News'),
        ('GLOBAL', 'Global'),
    ]

    title = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='posts')
    content = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='GLOBAL')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

class Comments(models.Model):
	commentor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	post = models.ForeignKey(Posts,on_delete=models.CASCADE,related_name='comments')
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.commentor.name} on {self.post.title}"
