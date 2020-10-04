import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.signals import post_save
from user.models import User, Profile
from faker import Factory


faker = Factory.create()


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    email = faker.email()
    username = faker.user_name()
    firstname = faker.first_name()
    lastname = faker.last_name()
    password = faker.password()
    profile = factory.RelatedFactory(
        'user.tests.factories.ProfileFactory', factory_related_name='user')


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Profile

    date_of_birth = faker.date_of_birth()
    image = factory.django.ImageField(filename="uploadedImage.jpg")
    user = factory.SubFactory(UserFactory, profile=None)
