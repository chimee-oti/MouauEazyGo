from django.test import TestCase
# import pytest
from user.models import User, Profile
# pytestmark = pytest.mark.django.db
from MouauEasyGo.settings import INSTALLED_APPS, AUTH_USER_MODEL
from django.db import transaction
from django.shortcuts import reverse
from django.core.files.uploadedfile import SimpleUploadedFile


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
        self.email = "test@gmail.com"
        self.username = "Nicknameuser"
        self.firstname = "Nicknamefirst"
        self.lastname = "Nicknamelast"
        self.password = "secretpassword"
        self.date_of_birth = "2002-04-05"

        self.user = User.objects.create_user(
            email=self.email,
            username=self.username,
            firstname=self.firstname,
            lastname=self.lastname,
            password=self.password
        )
     
        self.small_jpg = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.uploadedimage = SimpleUploadedFile(name='small.jpg', content=self.small_jpg, content_type='image/jpg')
        self.user.profile.image=self.uploadedimage
        self.user.profile.date_of_birth=self.date_of_birth
        self.user.profile.save()
        
    def test_image_location(self):
        assert self.user.profile.image.url == r'/media/profile_pics/small.jpg'
        
    def test_default_image(self):
        self.pro = Profile.objects.create(user=self.user, date_of_birth=self.date_of_birth)
        self.pro.save()
        
        assert self.pro.image.url == 'media/default.jpg'
        
    def test_str_object_return_user_profile(self):
        assert str(self.user.profile) == f"{self.user.username}'s profile"
        
    def test_get_absolute_url(self):
        self.detail_url = reverse('profile_detail', kwargs={pk: self.user.id})
        
        assert self.user.profile.get_absolute_url() == self.detail_url