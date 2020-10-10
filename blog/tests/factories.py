import factory
from blog.models import Post
from faker import Factory
from user.tests.factories import UserFactory
import pytest


fake = Factory.create()

class PostFactory(factory.django.DjangoModelFactory):
	
	class Meta:
		model = Post

	title = fake.lexify('?? ??? ??????')
	content = factory.Faker('text')
	author = factory.SubFactory(UserFactory)
	time_posted = factory.Faker('date_time_this_year')