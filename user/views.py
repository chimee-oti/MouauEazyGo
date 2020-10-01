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
from user.mixins import Update_view, UserMustBeAnoynmousMixin
from django.contrib.auth.forms import UserCreationForm


def user_register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            # email = form.cleaned_data.get('email')
            # firstname = form.cleaned_data.get('firstname')
            # lastname = form.cleaned_data.get('lastname')
            messages.success(request, f'Account created for {username}!')
            return redirect('user_profile_detail')
    else:
        form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form': form})


# class user_register_view(UserMustBeAnoynmousMixin, CreateView):
#     template_name = "user/register.html"
#     form_class = UserRegistrationForm
#     success_url = reverse_lazy('user_profile_detail')

#     def form_valid(self, form):
#         user = User.objects.create_user(email=form.cleaned_data['email'],
#                                         username=form.cleaned_data['username'],
#                                         firstname=form.cleaned_data['firstname'],
#                                         lastname=form.cleaned_data['lastname'],
#                                         password=form.cleaned_data['password1'])
#         user = authenticate(email=user.email, password=user.password)
#         if user is not None:
#             login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#         return redirect(self.success_url)


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
