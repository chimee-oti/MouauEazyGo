from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, views as auth_views
from django.views.generic.detail import DetailView
from user.models import Profile, User
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from user.forms import UserRegistrationForm, ProfileForm, UserForm
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from user.muiltiform import MultiFormsView


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


class update_view(LoginRequiredMixin, UserPassesTestMixin, MultiFormsView):
    template_name = "user/profile_update.html"
    form_classes = {'uForm': UserForm,
                    'pForm': ProfileForm}
    success_url = reverse_lazy("profile_detail")

    def get_uForm_initial(self):
        user = self.request.user
        return {'email': user.email,
                'username': user.username,
                'firstname': user.firstname,
                'lastname': user.lastname}

    def get_pForm_initial(self):
        profile = self.request.user.profile
        return {'image': profile.image,
                'about': profile.about,
                'date_of_birth': profile.date_of_birth,
                'country': profile.country}

    def get_context_data(self, **kwargs):
        context = super(update_view, self).get_context_data(**kwargs)
        context.update({"some context data": "data",
                        "some other context data": "another data"})
        return context

    def user_form_valid(self, form):
        user = self.request.user
        if form.cleaned_data['username']:
            user.username = form.cleaned_data['username']
        if form.cleaned_data['firstname']:
            user.firstname = form.cleaned_data['firstname']
        if form.cleaned_data['lastname']:
            user.lastname = form.cleaned_data['lastname']
        user.save()
        user = form.save(self.request)
        return form.uForm(self.request, user, self.get_success_url())

    def profile_form_valid(self, form):
        user = form.save(self.request)
        return form.pForm(self.request, user, self.get_success_url())
        
    def test_func(self):
        user = self.request.user 
        search_user = User.objects.get(pk=self.kwargs['pk'])
        if search_user == user:
            return true
        else
            redirect(reverse('profile_detail' user.id))
            return false


class profile_detail_view(DetailView):
    template_name = "user/profile_detail.html"
    model = Profile


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
