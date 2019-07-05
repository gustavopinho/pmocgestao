# coding=utf-8

from django.shortcuts import render
from django.views.generic import View
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin

from .models import User


class ProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    template_name = "accounts/profile.html"

    model = User
    fields = ['name', 'email']
    template_name_suffix = '_form'
    success_url = reverse_lazy('accounts:profile')
    success_message = 'Perfil atualizado com sucesso!'

    def get_object(self, queryset=None):
        obj = User.objects.get(id=self.request.user.id)
        return obj


class UpdatePasswordView(LoginRequiredMixin, SuccessMessageMixin, FormView):

    template_name = 'accounts/update_password.html'
    success_url = reverse_lazy('login')
    form_class = PasswordChangeForm
    success_message = 'Sua senha foi alterada, é necessário fazer o login novamente.'

    def get_form_kwargs(self):
        kwargs = super(UpdatePasswordView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(UpdatePasswordView, self).form_valid(form)



profile = ProfileView.as_view()
update_password = UpdatePasswordView.as_view()
