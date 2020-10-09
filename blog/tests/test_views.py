from django.test import TestCase, RequestFactory
from blog.tests.factories import PostFactory
from blog import views
from user.tests.factories import UserFactory
import pytest
from django.test.client import RequestFactory
from django.urls import reverse


@pytest.mark.skip
class TestPostListView(TestCase):
	def setUp(self):
		self.user1 = UserFactory()
		self.user2 = UserFactory()
		self.post = PostFactory()
		self.posts_user1 = PostFactory.create_batch(2, user=self.user1)
		self.posts_user2 = PostFactory(3, user=self.user2)
		self.request = RequestFactory().post(reverse('user-posts'), kwargs='username': self.user1.username)
		self.response = views.UserPostListView.as_view(self.request)
		
		
	def test_get_queryset_method(self):
		