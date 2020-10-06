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


class 


class TestUserProfileDetailView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_profile_detail_view(self):
        """test that user profile detail
        gets the correct user 's profile"""

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

    