from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, views as auth_views
from django.views.generic.detail import DetailView
from user.models import Profile, User
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.base import View
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
        return reverse('user_profile_detail')


class profile_update_view(LoginRequiredMixin, UserPassesTestMixin, MultiFormsView):
    template_name = "user/profile_update.html"
    form_classes = {'uForm': UserForm,
                    'pForm': ProfileForm}
    success_url = reverse_lazy("user_profile-detail")

    def get_uForm_initial(self):
        user = self.request.user
        return {'email': user.email,
                'username': user.username,
                'firstname': user.firstname,
                'lastname': user.lastname}

    def get_pForm_initial(self):
        profile = self.request.user.profile
        return {'image': profile.image,
                'date_of_birth': profile.date_of_birth}

    def get_context_data(self, **kwargs):
        context = super(profile_update_view, self).get_context_data(**kwargs)
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
        profile = self.request.user.profile
        if form.cleaned_data['image']:
            profile.image = form.cleaned_data['image']
        if form.cleaned_data['date_of_birth']:
            profile.date_of_birth = form.cleaned_data['date_of_birth']
        profile.save()
        user = form.save(self.request)
        return form.pForm(self.request, user, self.get_success_url())

    def test_func(self):
        user = self.request.user
        search_user = User.objects.get(pk=self.kwargs['pk'])
        if search_user == user:
            return True
        else:
            redirect(reverse('profile_detail', kwargs={pk: user.id}))
            return False


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
