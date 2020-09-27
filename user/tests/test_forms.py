from django.test import TestCase
from user.forms import UserRegistrationForm
from django.core.files.uploadedfile import SimpleUploadedFile
from base64 import b64decode
from django.core.files.base import ContentFile


class test_user_registration_form(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.image_data = b64decode(
            "R0lGODlhAQABAIABAP8AAP///yH5BAEAAAEALAAAAAABAAEAAAICRAEAOw==")
        cls.image_file = ContentFile(cls.image_data, 'one.jpg')
        cls.uploaded_image_file = SimpleUploadedFile(
            cls.image_file.name,
            cls.image_file.read(),
            content_type="image/png"
        )
        cls.form = UserRegistrationForm(data={
            "email": "test@gmail.com",
            "user_name": "myusername",
            "first_name": "myfirstname",
            "last_name": "mylastname",
            "date_of_birth": "3/3/5223",
            "country": "Nigeria",
            "image": "cls.uploaded_image_file",
            "about": "This is the fucking about"
        })

    
