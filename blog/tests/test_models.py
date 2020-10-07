from django.test import TestCase
from blog.models import Post
from faker import Faker
from user.tests.factories import UserFactory
from django.urls import reverse


class TestPostModel(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.faker = Faker()
        self.post = Post.objects.create(title=self.faker.lexify(
            '? ??? ??????'), content=self.faker.text(), author=self.user, time_posted=self.faker.date_time_this_year())

    def test_str_function(self):
        self.assertEqual(str(self.post), self.post.title)

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), reverse('blog:post-detail', kwargs={'pk': self.post.pk}))
