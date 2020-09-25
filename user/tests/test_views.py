# from django.test import TestCase, Client
# from django.test.client import RequestFactory
# from user.views import user_register_view
# from user.forms import UserRegistrationForm
# from django.shortcuts import reverse


# # patching the form doesn't work with the class based view
# # we need to patch classname.form_class instead
# @patch('user_registration_view.form_class')
# class UserRegistrationViewTest(TestCase):

#     # define the view
#     def register_view(self, request):
#         return user_register_view.as_view()(request)

#     def setup(self):
#         # we can't use HttpRequest() with a CBV
#         # we havve to use a RequestFactory instead.
#         self.form_data = {
#             'user_name': 'username',
#             'email': 'test@gmail.com',
#             'first_name': 'firstname',
#             'last_name': 'lastname',
#             'about': 'this is the about',
#             'date_of_birth': 'April 5, 2002',
#             'country': 'Nigeria'
#         }
#         self.request = RequestFactory().post(reverse('register_view'), data=self.form_data)
#         self.request.user = Mock()
#         self.request.session = {}

#     def test_passes_POST_data_to_user_register_view(self, mock_register_form):
#         self.register_view(self.request)