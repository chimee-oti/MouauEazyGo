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


class login_view(auth_views.LoginView):
    template_name = "user/login.html"


class logout_view(auth_views.LogoutView):
    template_name = "user/logout.html"

# direct the user to their profile page after registration


class user_register_view(CreateView):
    template_name = "user/register.html"
    form_class = UserRegistrationForm
    model = NewUser


    # I had to override the form_valid method and added form to the self parameter since get_success_url can't access form directly

    def form_valid(self, form):
        self.form = form
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
            data['name_of_user'] = self.request.GET.get('username')
        except KeyError:
            return data
        return data

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(name__startswith=self.kwargs[self.request.user.user_name])

    # if the user's username is in slug, then use it in the profile's url else then pick the username from the form and use instead
    def get_success_url(self):
        if self.request.GET.get('username'):
            return reverse('profile', args=(self.request.GET.get('username'))


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
class profile_update_view(UserPassesTestMixin, UpdateView):
    model = Profile
    fields = ['date_of_birth', 'country', 'about', 'image', ]
    template_name = 'user/profile_update_form.html'

    def get_object(self):
        user = self.request.user
        return get_object_or_404(Profile, pk=user.id)

    # try to get the user_name from the current user.
    # if the user is an Anoynmous user then just redirect to detail page
    def test_func(self):
        try:
            x = self.request.user.user_name
            y = self.kwargs.get('name_of_user')
            if x == y:
                return True
            else:
                return redirect('profile_detail_view.as_view()')
        except AttributeError:
            return redirect('profile_detail_view.as_view()')


# this is the profile page as viewed by the general public
# this view can only be reached if the current logged  in user
# is not the one access the view
class profile_detail_view(DetailView):
    template_name = "user/profile_detail.html"
    model = Profile

    def get_object(self):
        user = self.request.user
        return get_object_or_404(Profile.objects.get(pk=user.id))
