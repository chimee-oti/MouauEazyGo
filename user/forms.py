from django import forms
from user.models import Profile, User
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    date_of_birth = forms.DateField(required=True)
    image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['email', 'username', 'firstname',
                  'lastname', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'image', ]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'firstname', 'lastname', ]
