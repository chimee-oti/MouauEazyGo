from django.test import TestCase, Client
from user.forms import UserRegistrationForm
from io import BytesIO
from django.shortcuts import reverse
from django.contrib.auth import get_user_model


class TestUserRegistrationView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.img = BytesIO(b'mybinarydata')
        cls.img.name = 'myimage.jpg'

        cls.form_data = {
            "email": "test@gmail.com",
            "user_name": "myusername",
            "first_name": "myfirstname",
            "last_name": "mylastname",
            "password1": "SecretPassword1",
            "password2": "SecretPassword1",
            "date_of_birth": "3/3/5223",
            "country": "Nigeria",
            "image": cls.img,
            "about": "This is the fucking about"
        }


class TestViewGetMethodsNoLogin(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user_update = reverse('user_update')

    def test_login_view_get(self):
        self.response = self.client.get(self.login_url)

        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'user/login.html')
    

class TestViewGetMethodsLogin(TestCase):

    def setUp(self):
        self.client = Client()
        User = get_user_medel()
        user = User.objects.create()
        self.user_update = reverse('user_update')



    def test_user_update_view_get(self):
        self.response = self.client.get(self.user_update)

        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(
            self.response, 'user/user_update_form.html', 'user/profile_user_update_form.html')
