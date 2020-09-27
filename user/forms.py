from django import forms
from user.models import Profile, NewUser
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    date_of_birth = forms.DateField(required=True)
    country = forms.CharField(max_length=50, required=True)
    image = forms.ImageField(required=False)
    about = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = NewUser
        fields = ['email', 'user_name', 'first_name', 'last_name', ]

    # save profile info as well as the user info in the form
    def save(self, commit=True):
        if not commit:
            raise NotImplementedError(
                "Can't create User and UserProfile without database save")
        user = super(UserRegistrationForm, self).save(commit=True)
        user.save()
        profile, created = Profile.objects.get_or_create(user=user)
        profile.about = self.cleaned_data['about']
        profile.date_of_birth = self.cleaned_data['date_of_birth']
        profile.country = self.cleaned_data['country']
        profile.save()
        return user, profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'country', 'about', 'image',)


class UserForm(forms.ModelForm):
    class Meta:
        model = NewUser
        fields = ('user_name', 'first_name', 'last_name', )
