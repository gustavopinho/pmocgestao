from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy

from cliente.models import Atividade
from core.utils import get_empresa

class AtividadeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Atividade
    paginate_by = 20
    raise_exception = True
    permission_required = (
        'cliente.view_atividade'
    )

    def get_queryset(self):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])
        # Verificar se o usuário tem permissão para acessar essa empresa
        try:
            q = self.request.GET.get("q")
            object_list = cliente.atividades.filter(nome__icontains=q)
        except:
            object_list = cliente.atividades.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(AtividadeListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q", '')
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        context['cliente'] = context['empresa'].clientes.get(pk=self.kwargs['cliente'])
        return context


class AtividadeCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Atividade
    fields = ['nome']
    success_url = '/'
    success_message = 'Departamento criado com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.add_atividade'
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        self.success_url = reverse_lazy(
            'empresa:cliente:atividade_list',
            kwargs={"empresa" : empresa.pk, "cliente" : cliente.pk}
        )
        
        # Verificar se o usuário tem permissão para acessar essa empresa
        form.instance.cliente = cliente
        return super(AtividadeCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AtividadeCreateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        context['cliente'] = context['empresa'].clientes.get(pk=self.kwargs['cliente'])
        return context


class AtividadeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Atividade
    fields = ['nome']
    template_name_suffix = '_form'
    success_url = '/'
    success_message = 'Departamento atualizado com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.change_atividade',
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        self.success_url = reverse_lazy(
            'empresa:cliente:atividade_list',
            kwargs={"empresa" : empresa.pk, "cliente" : cliente.pk}
        )
        
        # Verificar se o usuário tem permissão para acessar essa empresa
        form.instance.cliente = cliente
        return super(AtividadeUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AtividadeUpdateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        context['cliente'] = context['empresa'].clientes.get(pk=self.kwargs['cliente'])
        return context


class AtividadeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Atividade
    success_url = '/'
    success_message = 'Departamento excluído com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.delete_atividade',
    )

    def get_object(self, queryset=None):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        self.success_url = reverse_lazy(
            'empresa:cliente:atividade_list',
            kwargs={"empresa" : empresa.pk, "cliente" : cliente.pk}
        )
        
        obj = cliente.atividades.get(pk=self.kwargs['pk'])
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(AtividadeDeleteView, self).delete(request, *args, **kwargs)


# Atividade
atividade_list = AtividadeListView.as_view()
atividade_create = AtividadeCreateView.as_view()
atividade_update = AtividadeUpdateView.as_view()
atividade_delete = AtividadeDeleteView.as_view()