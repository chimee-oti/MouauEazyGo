import factory
from faker import Faker
from .factories import UserFactory
from user import views
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
import pytest
pytestmark = pytest.mark.django_db

