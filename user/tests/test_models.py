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
        self.assertEqual(super_user.user_name, 'username1')
        self.assertEqual(super_user.first_name, 'firstname1')
        self.assertEqual(super_user.last_name, 'lastname1')
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)
        self.assertEqual(str(super_user), "username1")

        # test if your validations are working correctly
        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='test2@gmail.com', user_name='username2', first_name='first_name2', last_name='last_name2', password='password', is_superuser=False
            )

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='test3@gmail.com', user_name='username3', first_name='first_name3', last_name='last_name3', password='password', is_staff=False
            )

    # same checks used on superuser above was used here in user
    def test_new_user(self):
        db = get_user_model()
        user = db.objects.create_user(
            'test4@gmail.com', 'username4', 'firstname4', 'lastname4', 'password'
        )
        self.assertEqual(user.email, 'test4@gmail.com')
        self.assertEqual(user.user_name, 'username4')
        self.assertEqual(user.first_name, 'firstname4')
        self.assertEqual(user.last_name, 'lastname4')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_active)

        with self.assertRaises(ValueError):
            db.objects.create_user(
                email='', user_name='username5', first_name='first_name5', last_name='last_name5', password='password'
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
