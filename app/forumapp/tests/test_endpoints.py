# Test for the existing endpoints
from django.test import TestCase
from django.urls import reverse
from forumapp import models
from rest_framework.test import APIClient


class PostsTestCase(TestCase):
	def setUp(self):
		# Create a user
		self.user = models.User.objects.create_user(
			email='test@example.com',
            password='pass123',
            name='Test User'
            )

		# Create some posts

		self.post1 = models.Posts.objects.create(
			title='Post 1',
            content='Content 1',
            author=self.user
            )

		self.post2 = models.Posts.objects.create(
			title='Post 2',
            content='Content 2',
            author=self.user,
            )

		# We use APIClient and login
		self.client = APIClient()
		# We need to authenticate the user because of our permissions on the api/posts/ endpoint (IsAuthenticated)
		self.client.force_authenticate(user=self.user) 


	def test_list_posts(self):
		url = reverse('posts-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code , 200)
		self.assertEqual(len(response.json()), 2) # Because we created 2 posts

	def test_post_details(self):
		url = reverse('posts-detail', kwargs = {'pk':self.post1.id})
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200) # Check if the request status code is OK (200) as it should be
		data = response.json() # We jsonify the data so we can test the title,content and author
		self.assertEqual(data['title'], 'Post 1') 
		self.assertEqual(data['content'], 'Content 1')
		self.assertEqual(data['author'], self.user.name)

	def test_like_feature(self):
		url = reverse('posts-like', kwargs = {'pk': self.post2.id})

		# Add manually like to a post 
		self.post2.likes.add(self.user)
		# Refresh the database so it can get the new like
		self.post2.refresh_from_db()
		# Make the test
		self.assertEqual(self.post2.likes.count(), 1)

    	# We call the endpoint again (unlike the post)
		response = self.client.post(url)
		self.assertEqual(response.status_code, 200)
		self.post2.refresh_from_db()
		self.assertEqual(self.post2.likes.count(), 0)

	    # Call the endpoint again (user likes it)
		response = self.client.post(url)
		self.post2.refresh_from_db()
		self.assertEqual(self.post2.likes.count(), 1)  # User liked again

	def test_get_all_liked_posts(self):
		self.post1.likes.add(self.user)
		self.post2.likes.add(self.user)
		url = reverse('liked-posts')
		response = self.client.get(url)

		# Refresh posts to ensure the DB state is up-to-date
		self.post1.refresh_from_db()
		self.post2.refresh_from_db()

		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.json()), 2)  # user liked 2 posts



