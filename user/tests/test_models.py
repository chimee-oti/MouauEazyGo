from django.test import TestCase
from user.models import Profile
from django.contrib.auth import get_user_model
# since you are using a custom user models, the user models will
# be referenced with the get_user_model function


class TestUserAccounts(TestCase):

    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser(
            'test1@gmail.com', 'username1', 'firstname1', 'lastname1', 'password'
        )
        # create a superuser and test if the data was saved correctly
        self.assertEqual(super_user.email, 'test1@gmail.com')
        self.assertEqual(super_user.username, 'username1')
        self.assertEqual(super_user.firstname, 'firstname1')
        self.assertEqual(super_user.lastname, 'lastname1')
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)
        self.assertEqual(str(super_user), "username1")

        # test if your validations are working correctly
        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='test2@gmail.com', username='username2', firstname='firstname2', lastname='lastname2', password='password', is_superuser=False
            )

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='test3@gmail.com', username='username3', firstname='firstname3', lastname='lastname3', password='password', is_staff=False
            )

    # same checks used on superuser above was used here in user
    def test_new_user(self):
        db = get_user_model()
        user = db.objects.create_user(
            'test4@gmail.com', 'username4', 'firstname4', 'lastname4', 'password'
        )
        self.assertEqual(user.email, 'test4@gmail.com')
        self.assertEqual(user.username, 'username4')
        self.assertEqual(user.firstname, 'firstname4')
        self.assertEqual(user.lastname, 'lastname4')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_active)

        with self.assertRaises(ValueError):
            db.objects.create_user(
                email='', username='username5', firstname='firstname5', lastname='lastname5', password='password'
            )


class TestProfile(TestCase):

    @classmethod
    def setUpTestData(cls):
        db = get_user_model()
        # create a user
        cls.user = db.objects.create_user(
            'test@gmail.com', 'username', 'firstname', 'lastname', 'password'
        )

    def test_profile_str_object_is_working(self):
        # get the user's profile, this also shows that the profile
        # signal is working as expected
        user_profile = Profile.objects.get(user=self.user)
        self.assertEqual(str(user_profile), "username's profile")
