from django.views.generic.edit import FormView
from user.forms import UserUpdateForm, ProfileUpdateForm
from django.shortcuts import redirect


class Update_view(FormView):

    def post(self, request, *args, **kwargs):
        uForm = UserUpdateForm(request.POST, instance=request.user)
        pForm = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)

        if uForm.is_valid() and pForm.is_valid():
            return self.forms_valid(uForm, pForm)
        else:
            return self.forms_invalid(uForm, pForm)

    def forms_valid(self, uForm, pForm):
        uForm.save()
        pForm.save()
        return redirect(self.success_url)

    def forms_invalid(self, uForm, pForm):
        return self.render_to_response(self.get_context_data(uForm=uForm, pForm=pForm))

    def get(self, request, *args, **kwargs):
        self.uForm = UserUpdateForm(instance=request.user)
        self.pForm = ProfileUpdateForm(instance=request.user.profile)
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        if 'uForm' not in kwargs and 'pForm' not in kwargs:
            kwargs['uForm'] = UserUpdateForm(instance=self.request.user)
            kwargs['pForm'] = ProfileUpdateForm(
                instance=self.request.user.profile)
        return kwargs
