from django.test import TestCase, Client
from user.forms import UserRegistrationForm
from django.contrib.auth import get_user_model
from user.models import Profile


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

        # email is save to use because it is a unique field

    def setUp(self):
        self.client = Client()
        self.reponse = self.client.post('register/', data=self.form_data)
        self.user = get_user_model().objects.filter(email="test@gmail.com").first()
        self.profile = Profile.objects.get(user=self.user)

    def test_that_NewUser_data_is_saved(self):

        self.assertEqual(self.user.user_name, 'username')
        self.assertEqual(self.user.email, 'email')
        self.assertEqual(self.user.first_name, 'firstname')
        self.assertEqual(self.user.last_name, 'lastname'),

    def test_that_profile_data_is_saved(self):

        self.assertEqual(self.user.about, 'this is the about'),
        self.assertEqual(self.user.date_of_birth, 'April 5, 2002')
        self.assertEqual(self.user.country, 'Nigeria'),
