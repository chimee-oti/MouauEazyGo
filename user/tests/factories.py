import factory
from . import user
from django.core.files.uploadedfile import SimpleUploadedFile


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = User


    class Meta:
        model = 'user.User'

    # generate unique user and email fields
    email = factory.Sequence(lambda n : "user{}@email.com".format(n))
    username = factory.Sequence(lambda n : "user{}".format(n))
    firstname = "NameFirst"
    lastname = "NameLast"
    profile = factory.RelatedFactory(ProfileFactory, factory_related_name='user')
  

@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Profile
    
    
    class Meta:
        model = 'user.profile'
    
    image_content = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )
        
    date_of_birth = '2002-04-05'
    image = SimpleUploadedFile(name='small.jpg', content=image_content, content_type='image/jpg')
    user = factory.SubFactory('UserFactory', profile=None)