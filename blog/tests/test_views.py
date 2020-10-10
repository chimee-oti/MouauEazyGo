from django.test import TestCase, RequestFactory
from blog.tests.factories import PostFactory
from blog import views
from user.tests.factories import UserFactory
import pytest
from django.urls import reverse
from blog.models import Post



class TestPostListView(TestCase):
    def setUp(self):
        self.view = views.UserPostListView
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.url = reverse('blog:user-posts',
                           kwargs={'username': self.user1.username})
        self.posts_user1 = PostFactory.create_batch(2, author=self.user1)
        self.request = RequestFactory().get(self.url)
        self.response = self.view.as_view()(self.request, username = self.user1.username)
        
    def test_get_queryset(self):
        user1_post_queryset = Post.objects.filter(author=self.user1).order_by('-time_posted')
        self.assertIsInstance(self.response.context_data, dict)
        self.assertEqual(list(self.response.context_data['posts']), list(user1_post_queryset))
