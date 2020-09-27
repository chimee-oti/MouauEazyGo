from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, views as auth_views
from django.views.generic.detail import DetailView
from user.models import Profile, NewUser
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from user.forms import ProfileForm, UserForm, UserRegistrationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login


class user_register_view(CreateView):
    template_name = "user/register.html"
    form_class = UserRegistrationForm

    # login user if form is valid and form data has been saved
    def form_valid(self, form):
        self.object = form.save()
        new_user = authenticate(
            email=form.cleaned_data['email'], password=form.cleaned_data['password1'], )
        login(self.request, new_user)
        return super().form_valid(form)

    # direct the user to their profile page after registration
    def get_success_url(self):
        return reverse('profile')

# view for user to update their details
# this will inherit from the same template with profile update


class user_update_view(UpdateView):
    model = NewUser
    template_name = 'user/user_update_form.html'
    form_class = UserForm

    def get_object(self):
        user = self.request.user
        return get_object_or_404(NewUser, pk=user.id)


# view for user to update their details
# this will inherit from the same template with user update
class profile_update_view(UpdateView):
    model = Profile
    template_name = 'user/profile_update_form.html'
    form_class = ProfileForm

    def get_object(self):
        user = self.request.user
        return get_object_or_404(Profile, pk=user.id)


class profile_detail_view(DetailView):
    template_name = "user/profile_detail.html"
    model = Profile

    def get_object(self):
        user = self.request.user
        return get_object_or_404(Profile.objects.get(pk=user.id))


class login_view(auth_views.LoginView):
    template_name = "user/login.html"


class logout_view(auth_views.LogoutView):
    template_name = "user/logout.html"


class password_change_view(auth_views.PasswordChangeView):
    template_name = "user/password_change_form.html"


class password_change_done_view(auth_views.PasswordChangeDoneView):
    template_name = "user/password_change_done.html"


class password_reset_view(auth_views.PasswordResetView):
    template_name = "user/password_reset.html"


class password_reset_done_view(auth_views.PasswordResetDoneView):
    template_name = "user/password_reset_done.html"


class password_reset_confirm_view(auth_views.PasswordResetConfirmView):
    template_name = "user/password_reset_confirm_done.html"


class password_reset_complete_view(auth_views.PasswordResetCompleteView):
    template_name = "user/password_reset_complete.html"
