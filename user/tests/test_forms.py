from django.test import TestCase, Client
from user.forms import UserRegistrationForm
from django.contrib.auth import get_user_model
from user.models import Profile, NewUser
from django.shortcuts import reverse


class TestRegistrationForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.form_data = {
            'user_name': 'username',
            'email': 'test@gmail.com',
            'first_name': 'firstname',
            'last_name': 'lastname',
            'about': 'this is the about',
            'date_of_birth': 'April 5, 2002',
            'country': 'Nigeria'
        }
        cls.register_url = reverse('register')

        # email is save to use because it is a unique field

    def setUp(self):
        self.client = Client()
        self.reponse = self.client.post(self.register_url, data=self.form_data)
        self.user = get_user_model().objects.filter(email="test@gmail.com").first()
        self.profile = Profile.objects.filter(user=self.user)

    def test_that_NewUser_data_is_saved(self):

        self.assertEqual(NewUser._meta.get_field(
            'user_name').value_from_object(self.user), 'username')
        self.assertEqual(NewUser._meta.get_field('email').value_from_object(self.user), 'email')
        self.assertEqual(NewUser._meta.get_field(
            'first_name').value_from_object(self.user), 'firstname')
        self.assertEqual(NewUser._meta.get_field(
            'last_name').value_from_object(self.user), 'lastname'),

    def test_that_profile_data_is_saved(self):

        self.assertEqual(self.profile.about, 'this is the about'),
        self.assertEqual(self.profile.date_of_birth, 'April 5, 2002')
        self.assertEqual(self.profile.country, 'Nigeria'),
