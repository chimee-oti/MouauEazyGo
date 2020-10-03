from django.test import TestCase, Client
from user.forms import UserRegistrationForm
from io import BytesIO
from django.shortcuts import reverse
from user.models import User


class TestUserRegistrationView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.img = BytesIO(b'mybinarydata')
        cls.img.name = 'myimage.jpg'

        cls.form_data = {
            "email": "test@gmail.com",
            "username": "myusername",
            "firstname": "myfirstname",
            "lastname": "mylastname",
            "password1": "SecretPassword1",
            "password2": "SecretPassword1",
            "date_of_birth": "3/3/5223",
            "image": cls.img
        }

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.response_register = self.client.post(
            self.register_url, self.form_data)
        self.user = User.objects.filter(email="test@gmail.com").first()

    def test_that_user_is_created(self):

        self.assertEqual(self.user.email, "test@gmail.com")
        self.assertEqual(self.user.username, "myusername")
        self.assertEqual(self.user.firstname, "myfirstname")
        self.assertEqual(self.user.lastname, "mylastname")
        self.assertEqual(self.user.password, "SecretPassword1")

    def test_that_user_profile_is_created(self):
        self.profile = self.user.profile

        self.assertEqual(self.profile.date_of_birth, "3/3/5223")
        self.assertEqual(self.profile.image, self.img)


class TestViewGetMethodsNoLogin(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')

    def test_login_view_get(self):
        self.response = self.client.get(self.login_url)

        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'user/login.html')


class TestViewGetMethodsLogin(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')

        self.user1 = User.objects.create(
            email='user1@gmail.com', username='user1', firstname='firstuser1', lastname='lastuser1')
        self.user1.set_password = "password1"
        self.client.post(self.login_url, {
                         'email': self.user1.email, 'password': self.user1.password}, follow=False)
        self.profile_update_url = reverse(
            'profile_update', kwargs={'pk': self.user1.id})

    def test_profile_update_view_get(self):
        self.response = self.client.get(self.profile_update_url)

        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(
            self.response, 'user/profile_update.html', 'user/base.html')

    def test_user_is_redirected_if_not_their_profile(self):
        """test that the a user is redirected to their own profile page, if they try to 
        access the update page of another user 's profile"""

        self.user2 = User.objects.create(
            email='user2@gmail.com', username='user2', firstname='firstuser2', lastname='lastuser2')
        self.user2.set_password = "password2"
        self.profile_update_url_2 = reverse(
            'profile_update', kwargs={'pk': self.user2.id})
        response_update = self.client.get(self.profile_update_url)

        self.assertEqual(response_update.status_code, 302)
