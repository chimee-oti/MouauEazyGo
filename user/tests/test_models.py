from django.test import TestCase
from user.models import User, Profile
from MouauEasyGo.settings import INSTALLED_APPS, AUTH_USER_MODEL
from django.db import transaction
from django.shortcuts import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from user.tests.factories import UserFactory, ProfileFactory


class TestSettings(TestCase):
    def test_account_configuration(self):
        assert 'user.apps.UserConfig' in INSTALLED_APPS
        assert 'user.User' == AUTH_USER_MODEL
