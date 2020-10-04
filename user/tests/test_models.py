from django.test import TestCase
# import pytest
from user.models import User, Profile
# pytestmark = pytest.mark.django.db
from MouauEasyGo.settings import INSTALLED_APPS, AUTH_USER_MODEL
from django.db import transaction
from django.shortcuts import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from user.tests.factories import UserFactory, ProfileFactory


class TestSettings(TestCase):
    def test_account_configuration(self):
        assert 'user.apps.UserConfig' in INSTALLED_APPS
        assert 'user.User' == AUTH_USER_MODEL


class TestUserCreateSuperuser(TestCase):

    def setUp(self):
        self.email = "test@gmail.com"
        self.username = "Nicknameuser"
        self.firstname = "Nicknamefirst"
        self.lastname = "Nicknamelast"
        self.password = "secretpassword"

        self.superuser = User.objects.create_superuser(
            email=self.email,
            username=self.username,
            firstname=self.firstname,
            lastname=self.lastname,
            password=self.password
        )

    def test_create_superuser(self):
        assert isinstance(self.superuser, User)

    def test_is_staff(self):
        assert self.superuser.is_staff

    def test_is_superuser(self):
        assert self.superuser.is_superuser

    def test_is_active(self):
        assert self.superuser.is_active

    def test_email_saved(self):
        assert self.superuser.email == self.email

    def test_username_saved(self):
        assert self.superuser.username == self.username

    def test_firstname_saved(self):
        assert self.superuser.firstname == self.firstname

    def test_lastname_saved(self):
        assert self.superuser.lastname == self.lastname

    def test_password_hashed(self):
        assert not self.superuser.password == self.password

    def test_password_saved(self):
        assert self.superuser.check_password("secretpassword")

    def test_is_staff_raises_exception_if_False(self):
        with self.assertRaises(ValueError, msg='Superuser must be assigned to is_staff=True.'):
            with transaction.atomic():
                User.objects.create_superuser(
                    email=self.email,
                    username=self.username,
                    firstname=self.firstname,
                    lastname=self.lastname,
                    password=self.password,
                    is_staff='False')

    def test_is_superuser_raises_exception_if_False(self):
        with self.assertRaises(ValueError, msg='Superuser must be assigned to is_superuser=True.'):
            with transaction.atomic():
                User.objects.create_superuser(
                    email=self.email,
                    username=self.username,
                    firstname=self.firstname,
                    lastname=self.lastname,
                    password=self.password,
                    is_superuser='False')


class TestUserCreateUser(TestCase):

    def setUp(self):
        self.email = "test@gmail.com"
        self.username = "Nicknameuser"
        self.firstname = "Nicknamefirst"
        self.lastname = "Nicknamelast"
        self.password = "secretpassword"

        self.user = User.objects.create_user(
            email=self.email,
            username=self.username,
            firstname=self.firstname,
            lastname=self.lastname,
            password=self.password
        )

    def test_create_user(self):
        assert isinstance(self.user, User)

    def test_not_is_staff(self):
        assert not self.user.is_staff

    def test_not_is_superuser(self):
        assert not self.user.is_superuser

    def test_not_is_active(self):
        assert not self.user.is_active

    def test_email_saved(self):
        assert self.user.email == self.email

    def test_username_saved(self):
        assert self.user.username == self.username

    def test_firstname_saved(self):
        assert self.user.firstname == self.firstname

    def test_lastname_saved(self):
        assert self.user.lastname == self.lastname

    def test_password_hashed(self):
        assert not self.user.password == self.password

    def test_password_saved(self):
        assert self.user.check_password("secretpassword")

    def test_not_email_raises_exception(self):
        with self.assertRaises(ValueError, msg='You must provide an email address'):
            with transaction.atomic():
                User.objects.create_user(
                    email="",
                    username=self.username,
                    firstname=self.firstname,
                    lastname=self.lastname,
                    password=self.password)

    def test_str_object_return_username(self):
        assert str(self.user) == self.user.username


class TestProfile(TestCase):

    def setUp(self):
        self.user1 = UserFactory()

    def test_image_location(self):
        assert self.user1.profile.image.url == f'/media/{self.user1.profile.image.name}'

    def test_str_object_return_user_profile(self):
        assert str(self.user1.profile) == f"{self.user1.username}'s profile"

    def test_get_absolute_url(self):
        self.detail_url = '/user/profile/1'

        assert self.user1.profile.get_absolute_url() == self.detail_url
