from django import forms
from user.models import Profile, User
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm


class UserRegistrationForm(UserCreationForm):
    date_of_birth = forms.DateField(required=True)
    image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['email', 'username', 'firstname',
                  'lastname', 'password1', 'password2', 'date_of_birth', 'image']


class CustomSignupForm(SignupForm):
    username = forms.CharField(max_length=30, label='Username')
    firstname = forms.CharField(max_length=30, label='First Name')
    lastname = forms.CharField(max_length=30, label='Last Name')

    def signup(self, request, user):
        user.username = self.cleaned_data['username']
        user.firstname = self.cleaned_data['firstname']
        user.lastname = self.cleaned_data['lastname']
        user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'image', ]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'firstname', 'lastname', ]
