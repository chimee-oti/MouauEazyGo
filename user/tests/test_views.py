from django.utils.translation import gettext_lazy as _
from django.shortcuts import render
import factory
from faker import Faker
from .factories import UserFactory
from user import views
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase, Client
import pytest
from user.models import User, Profile
from django.http import Http404
from user.forms import UserRegistrationForm


class TestRegisterView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.data = {
            'username': self.user.username,
            'firstname': self.user.firstname,
            'lastname': self.user.lastname,
            'email': self.user.email,
            'password1': self.user.password,
            'password2': self.user.password,
            'date_of_birth': self.user.profile.date_of_birth,
            'image': self.user.profile.image
        }
        self.url = reverse('register')
        self.request = RequestFactory().post(self.url, data=self.data)
        
        self.request.user = self.user 
        self.response = views.user_register_view(self.request)
        self.saved_user = User.objects.filter(username=self.user.username).first()
    
    
    def test_user_now_exists(self):
        self.assertTrue(self.saved_user)
    
    def test_user_dateOfBirth_saved(self):
        self.assertEqual(self.saved_user.profile.date_of_birth, self.data['date_of_birth'])
        
    def test_user_image_saved(self):
        self.assertEqual(self.saved_user.profile.image, self.data['image'])
      
        
class TestUserProfileDetailView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_profile_detail_view(self):
        """test that user profile detail
        gets the correct user's profile"""

        user = UserFactory()
        url = reverse('user_profile_detail')
        factory = RequestFactory()
        request = factory.get(url)
        request.user = user
        response = views.user_profile_detail_view.as_view()(request)
        self.assertEqual(
            views.user_profile_detail_view.get_queryset(views.user_profile_detail_view)[0], Profile.objects.filter(user=user).first())

    def test_user_no_profile_get_object_exception(self):
        user = UserFactory(profile=None)
        url = reverse('user_profile_detail')
        factory = RequestFactory()
        request = factory.get(url)
        request.user = user

        with self.assertRaises(Http404):
            response = views.user_profile_detail_view.as_view()(request)


class TestLoginView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_already_login_redirects(self):
        user = UserFactory()
        request = RequestFactory().post(
            reverse('login'), {'username': user.username, 'password': user.password})
        request.user = user

        self.assertTrue(request.user.is_authenticated)
        response = views.login_view.as_view()(request)

        self.assertEqual(response.status_code, 302)

    def test_user_not_login_in_works(self):
        request = RequestFactory().get(reverse('login'))
        request.user = AnonymousUser()

        self.assertFalse(request.user.is_authenticated)
        response = views.login_view.as_view()(request)

        self.assertEqual(response.status_code, 200)

    