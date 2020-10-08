from user.backend import UserBackend
from django.test import TestCase
from user.tests.factories import UserFactory


class TestUserBackend(TestCase):
    def test_authenticate(self):
        user = UserFactory()
        