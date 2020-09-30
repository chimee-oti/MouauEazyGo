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

    # save profile info as well as the user info in the form
    def save(self, commit=False):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(user.password)
        user.save()
        profile, created = Profile.objects.get_or_create(user=user)
        profile.date_of_birth = self.cleaned_data['date_of_birth']
        profile.image = self.cleaned_data['image']
        profile.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'image', ]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'firstname', 'lastname', ]
