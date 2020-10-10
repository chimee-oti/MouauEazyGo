from django.test import TestCase, RequestFactory, Client
from user.mixins import Update_view
from user.tests.factories import UserFactory
from user import views
from faker import Faker
import factory
from django.urls import reverse
from user.models import User
import pytest



class TestUpdateViewMixin(TestCase):

    def setUp(self):
        self.fake = Faker()
        self.view = views.update_profile()
        self.user = UserFactory()
        self.client = Client()
        self.client.login(username=self.user.username,
                          password=self.user.password)
        self.data = {
            'email': self.fake.email(),
            'username': self.fake.user_name(),
            'firstname': self.fake.first_name(),
            'lastname': self.fake.last_name(),
            'date_of_birth': self.fake.date_of_birth(),
            'image': factory.django.ImageField(filename="NewImage.jpg")
        }
        self.request = RequestFactory.post(
            reverse('profile_update'), self.data, follow=False)
        self.request.user = self.user
        self.response = views.update_profile.as_view()(self.request)
        self.response.client = Client()
        self.user.refresh_from_db()
        
    def test_success_url_redirect(self):
    	self.assertEqual(self.response.status_code, 302)
    	self.assertRedirects(self.response, reverse('user_profile_detail'), fetch_redirect_response=False)
    	
    def test_email_updated(self):
    	view = views.update_profile
    	self.assertEqual(self.user.email, self.data.get('email', ''))