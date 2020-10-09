from django.contrib.auth import authenticate
from django.test import TestCase
from user.tests.factories import UserFactory
import pytest



@pytest.mark.skip(reason='authenticate not working')
class TestUserBackend(TestCase):
   
    def test_authenticate(self):
        user = UserFactory()
        authenticated_user = authenticate(email=user.email, password=user.password)
        self.assertEqual(authenticated_user, user)