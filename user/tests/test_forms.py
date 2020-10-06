from django.test import TestCase
from user.forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from faker import Faker
import factory


class Test_UserRegistrationForm(TestCase):

    def setUp(self):
        self.fakeUser = Faker()
        self.data = {
            'email': self.fakeUser.email(),
            'username': self.fakeUser.user_name(),
            'firstname': self.fakeUser.first_name(),
            'lastname': self.fakeUser.last_name(),
            'password1': 'secretdeadlypassword',
            'password2': 'secretdeadlypassword',
            'date_of_birth': self.fakeUser.date_of_birth(),
            'image': factory.django.ImageField(filename="uploadedImage.jpg")
        }
        self.form = UserRegistrationForm(data=self.data)

    def test_form_is_valid(self):
        self.assertTrue(self.form.is_valid())


class TestProfileUpdateForm(TestCase):

    def setUp(self):
        self.fakeProfile = Faker()
        self.data = {
            'date_of_birth': self.fakeProfile.date_of_birth(),
            'image': factory.django.ImageField(filename="uploadedImage.jpg")
        }
        self.form = ProfileUpdateForm(data=self.data)

    def test_form_is_valid(self):
        assert self.form.is_valid()


class TestUserUpdateForm(TestCase):

    def setUp(self):
        self.fakeUser = Faker()
        self.data = {
            'username': self.fakeUser.user_name(),
            'firstname': self.fakeUser.first_name(),
            'lastname': self.fakeUser.last_name()
        }
        self.form = UserUpdateForm(data=self.data)

    def test_form_is_valid(self):
        assert self.form.is_valid()
