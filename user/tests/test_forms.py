from django.test import TestCase
from user.forms import UserRegistrationForm
from io import BytesIO


class TestUserRegistrationForm(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.img = BytesIO(b'mybinarydata')
        cls.img.name = 'myimage.jpg'

    def test_that_form_data_is_valid(self):
        form = UserRegistrationForm(data={
            "email": "test@gmail.com",
            "username": "myusername",
            "firstname": "myfirstname",
            "lastname": "mylastname",
            "password1": "SecretPassword1",
            "password2": "SecretPassword1",
            "date_of_birth": "5/4/2002",
            "country": "Nigeria",
            "image": self.img,
            "about": "This is the fucking about"
        })

        self.assertTrue(form.is_valid())

    def test_form_with_no_data(self):
        form = UserRegistrationForm(data={})

        self.assertFalse(form.is_valid())
        # image and about fields are not required
        self.assertEqual(len(form.errors), 8)
