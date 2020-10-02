import factory


class UserFactory(factory.DjangoModelFactory):

    class Meta:
        model = 'user.User'
        django_get_or_create = ('email', 'username', 'firstname', 'lastname', )

    email = "test@gmail.com"
    username = "username"
    firstname = "firstname"
    lastname = "lastname"
