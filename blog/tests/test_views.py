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
		self.view = views.UserPostListView
		self.user1 = UserFactory()
		self.user2 = UserFactory()
		self.url = reverse('blog:user-posts', kwargs={'username': self.user1.username})
		self.post = PostFactory()
		self.posts_user1 = PostFactory.create_batch(2, author=self.user1)
		self.posts_user2 = PostFactory.create_batch(3, author=self.user2)
		self.request = RequestFactory().get(self.url)
		self.response = self.view.as_view()(self.request)

	def test_get_queryset_method(self):
		context = self.views.get_queryset(self.views)
		user1_post_queryset = Post.objects.filter(author=user1).order_by('-time_posted')
		self.assertQuerysetEqual(context, user_post_queryset)


class Testqueryset(TestCase):
	def test_get_queryset(method):
		view = views.UserPostListView
		user1 = UserFactory()
		user2 = UserFactory()
		url = reverse('blog:user-posts', kwargs={'username': user1.username})
		posts_user1 = PostFactory.create_batch(2, author=user1)
		posts_user2 = PostFactory.create_batch(3, author=user2)
		request = RequestFactory().get(url)
		response = view.as_view()(request)
		context = views.get_queryset(views)
		user1_post_queryset = Post.objects.filter(author=user1).order_by('-time_posted')
		self.assertQuerysetEqual(context, user_post_queryset)
