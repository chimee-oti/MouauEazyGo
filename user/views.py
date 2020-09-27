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


class login_view(auth_views.LoginView):
    template_name = "user/login.html"


class logout_view(auth_views.LogoutView):
    template_name = "user/logout.html"

# direct the user to their profile page after registration


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

    def get_success_url(self):
        return reverse('profile')


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


# this is the profile page as viewed by the owner of the profile
# the viewer passes the test only if they are the logged in user
# if they are not, then they are redirected to the the
# profile_detail_view.
class profile_update_view(UpdateView):
    model = Profile
    fields = ['date_of_birth', 'country', 'about', 'image', ]
    template_name = 'user/profile_update_form.html'

    def get_object(self):
        user = self.request.user
        return get_object_or_404(Profile, pk=user.id)


# this is the profile page as viewed by the general public
# this view can only be reached if the current logged  in user
# is not the one access the view
class profile_detail_view(DetailView):
    template_name = "user/profile_detail.html"
    model = Profile

    def get_object(self):
        user = self.request.user
        return get_object_or_404(Profile.objects.get(pk=user.id))
