from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy

from cliente.models import Unidade
from core.utils import get_empresa

class UnidadeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Unidade
    paginate_by = 20
    raise_exception = True
    permission_required = (
        'cliente.view_unidade'
    )

    def get_queryset(self):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])
        # Verificar se o usuário tem permissão para acessar essa empresa
        try:
            q = self.request.GET.get("q")
            object_list = cliente.unidades.filter(nome__icontains=q)
        except:
            object_list = cliente.unidades.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(UnidadeListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q", '')
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        context['cliente'] = context['empresa'].clientes.get(pk=self.kwargs['cliente'])
        return context


class UnidadeDetailView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DetailView):
    model = Unidade
    raise_exception = True
    permission_required = (
        'cliente.view_unidade'
    )

    def get_object(self, queryset=None):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])
        obj = cliente.unidades.get(pk=self.kwargs['pk'])

        return obj


class UnidadeCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Unidade
    fields = [
        'nome', 'responsavel', 'logradouro',
        'numero', 'complemento', 'bairro', 
        'cidade', 'uf', 'cep',
        'email', 'fone', 'celular'
    ]
    success_url = '/'
    success_message = 'Unidade criada com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.add_unidade'
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        self.success_url = reverse_lazy(
            'empresa:cliente:unidade_list',
            kwargs={"empresa" : empresa.pk, "cliente" : cliente.pk}
        )
        
        # Verificar se o usuário tem permissão para acessar essa empresa
        form.instance.cliente = cliente
        return super(UnidadeCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UnidadeCreateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        context['cliente'] = context['empresa'].clientes.get(pk=self.kwargs['cliente'])
        return context

    def get_form(self, form_class=None):    
        form = super(UnidadeCreateView, self).get_form(form_class)
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        form.fields["responsavel"].queryset = empresa.responsaveis.all()
        return form


class UnidadeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Unidade
    fields = [
        'nome', 'responsavel', 'logradouro',
        'numero', 'complemento', 'bairro', 
        'cidade', 'uf', 'cep',
        'email', 'fone', 'celular'
    ]
    template_name_suffix = '_form'
    success_url = '/'
    success_message = 'Unidade atualizada com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.change_unidade',
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        self.success_url = reverse_lazy(
            'empresa:cliente:unidade_list',
            kwargs={"empresa" : empresa.pk, "cliente" : cliente.pk}
        )
        
        # Verificar se o usuário tem permissão para acessar essa empresa
        form.instance.cliente = cliente
        return super(UnidadeUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UnidadeUpdateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        context['cliente'] = context['empresa'].clientes.get(pk=self.kwargs['cliente'])
        return context

    def get_form(self, form_class=None):    
        form = super(UnidadeUpdateView, self).get_form(form_class)
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        form.fields["responsavel"].queryset = empresa.responsaveis.all()
        return form


class UnidadeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Unidade
    success_url = '/'
    success_message = 'Unidade excluída com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.delete_unidade',
    )

    def get_object(self, queryset=None):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        self.success_url = reverse_lazy(
            'empresa:cliente:unidade_list',
            kwargs={"empresa" : empresa.pk, "cliente" : cliente.pk}
        )
        
        obj = cliente.unidades.get(pk=self.kwargs['pk'])
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(UnidadeDeleteView, self).delete(request, *args, **kwargs)


# Unidade
unidade_list = UnidadeListView.as_view()
unidade_create = UnidadeCreateView.as_view()
unidade_detail = UnidadeDetailView.as_view()
unidade_update = UnidadeUpdateView.as_view()
unidade_delete = UnidadeDeleteView.as_view()