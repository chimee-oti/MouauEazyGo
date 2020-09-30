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


class user_register_view(CreateView):
    template_name = "user/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user_profile_detail')

    def form_valid(self, form):
        self.user = form.save()
        if self.request.user is not None:
            logout(self.request)
        login(self.request, self.user)
        return redirect(self.success_url)


class update_class(Update_view):
    """inheriting the main deadly mixin I wrote"""
    success_url = reverse_lazy('user_profile_detail')
    template_name = "user/profile_update.html"


class profile_detail_view(DetailView):
    template_name = "user/profile_detail.html"
    model = Profile


class user_profile_detail(LoginRequiredMixin, DetailView):
    template_name = "user/profile_detail.html"
    model = Profile

    def get_object(self, queryset=None):
        """
        Return the object the view is displaying.
        Require `self.queryset` and a `pk` or `slug` argument in the URLconf.
        Subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()
        # Next, try looking up by primary key.
        # pk is now that of the current logged in user
        pk = self.request.user.id
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})
        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


class login_view(UserPassesTestMixin, auth_views.LoginView):
    template_name = "user/login.html"

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return True
        if user.is_authenticated:
            redirect(reverse('user_profile_detail'))
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
