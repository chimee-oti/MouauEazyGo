from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from user.models import Profile, User
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.base import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from user.forms import UserRegistrationForm, ProfileUpdateForm, UserUpdateForm
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from user.mixins import Update_view, UserAlreadyLoggedInTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.utils.translation import gettext_lazy as _


class user_register_view(CreateView):
    template_name = "user/register.html"
    form_class = UserRegistrationForm
    model = User

    def form_valid(self, form):
        self.object = form.save()
        profile = Profile.objects.filter(user=self.object).first()
        profile.date_of_birth = form.cleaned_data['date_of_birth']
        profile.image = form.cleaned_data['image']
        profile.save()
        return super(user_register_view, self).form_valid(form)


class update_profile(LoginRequiredMixin, Update_view):
    """inheriting the main deadly mixin I wrote"""
    success_url = reverse_lazy('user_profile_detail')
    template_name = "user/profile_update.html"


class profile_detail_view(DetailView):
    template_name = "user/profile_detail.html"
    model = Profile


class user_profile_detail_view(LoginRequiredMixin, DetailView):
    template_name = "user/profile_detail.html"
    model = Profile

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.request.user.id
        queryset = queryset.filter(pk=pk)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


class login_view(UserAlreadyLoggedInTestMixin, auth_views.LoginView):
    template_name = "user/login.html"

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return True
        if user.is_authenticated:
            return False


class logout_view(auth_views.LogoutView):
    template_name = "user/logout.html"


class password_change_view(LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = "user/password_change_form.html"


class password_change_done_view(LoginRequiredMixin, auth_views.PasswordChangeDoneView):
    template_name = "user/password_change_done.html"


class password_reset_view(auth_views.PasswordResetView):
    template_name = "user/password_reset.html"


class password_reset_done_view(auth_views.PasswordResetDoneView):
    template_name = "user/password_reset_done.html"


class password_reset_confirm_view(auth_views.PasswordResetConfirmView):
    template_name = "user/password_reset_confirm_done.html"


class password_reset_complete_view(auth_views.PasswordResetCompleteView):
    template_name = "user/password_reset_complete.html"
