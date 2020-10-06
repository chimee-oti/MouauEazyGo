from django.test import TestCase, RequestFactory, Client
from user.mixins import Update_view
from user.tests.factories import UserFactory
from user import views
from faker import Faker
import factory
from django.urls import reverse
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
        self.request = RequestFactory().post(
            'profile_update', data=self.data, follow=True)
        self.request.user = self.user
        self.response = views.update_profile.as_view()(self.request)
        self.response.client = Client()
