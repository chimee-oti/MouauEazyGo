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
from user.mixins import Update_view
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.utils.translation import gettext_lazy as _




def user_register_view(request):
    form = UserRegistrationForm(request.POST, request.FILES)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.profile.date_of_birth = form.cleaned_data.get('date_of_birth')
        user.profile.image = form.cleaned_data.get('image')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        # user = authenticate(username=username, password=password)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('user_profile_detail')
    else:
        form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form': form})
    

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


class login_view(auth_views.LoginView):
    template_name = "user/login.html"


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
