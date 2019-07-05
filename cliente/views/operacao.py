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

from cliente.models import Operacao
from core.utils import get_empresa

class OperacaoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Operacao
    paginate_by = 20
    raise_exception = True
    permission_required = (
        'cliente.view_operacao'
    )

    def get_queryset(self):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        try:
            q = self.request.GET.get("q")
            object_list = cliente.operacoes.filter(nome__icontains=q)
        except:
            object_list = cliente.operacoes.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(OperacaoListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q", '')
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        context['cliente'] = context['empresa'].clientes.get(pk=self.kwargs['cliente'])
        return context


class OperacaoCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Operacao
    fields = ['codigo', 'nome', 'grupo', 'intervalo', 'ativo']
    success_url = '/'
    success_message = 'Operação criada com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.add_operacao'
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        self.success_url = reverse_lazy(
            'empresa:cliente:operacao_list',
            kwargs={"empresa" : empresa.pk, 'cliente' : cliente.pk}
        )
        
        form.instance.cliente = cliente
        return super(OperacaoCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(OperacaoCreateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        context['cliente'] = context['empresa'].clientes.get(pk=self.kwargs['cliente'])
        return context

    def get_form(self, form_class=None):    
        form = super(OperacaoCreateView, self).get_form(form_class)
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])
        
        form.fields["grupo"].queryset = cliente.operacao_grupo.all()
        form.fields["intervalo"].queryset = empresa.manutencao_intervalo.all()
        return form


class OperacaoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Operacao
    fields = ['codigo', 'nome', 'grupo', 'intervalo', 'ativo']
    template_name_suffix = '_form'
    success_url = '/'
    success_message = 'Operação atualizada com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.change_operacao',
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        self.success_url = reverse_lazy(
            'empresa:cliente:operacao_list',
            kwargs={"empresa" : empresa.pk, 'cliente' : cliente.pk}
        )
        
        form.instance.cliente = cliente
        return super(OperacaoUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(OperacaoUpdateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        context['cliente'] = context['empresa'].clientes.get(pk=self.kwargs['cliente'])
        return context

    def get_form(self, form_class=None):    
        form = super(OperacaoUpdateView, self).get_form(form_class)
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])
        
        form.fields["grupo"].queryset = cliente.operacao_grupo.all()
        form.fields["intervalo"].queryset = empresa.manutencao_intervalo.all()
        return form


class OperacaoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Operacao
    success_url = '/'
    success_message = 'Operação excluída com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.delete_operacao',
    )

    def get_object(self, queryset=None):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        self.success_url = reverse_lazy(
            'empresa:cliente:operacao_list',
            kwargs={"empresa" : empresa.pk, 'cliente' : cliente.pk}
        )
        
        obj = cliente.operacoes.get(pk=self.kwargs['pk'])
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(OperacaoDeleteView, self).delete(request, *args, **kwargs)


# Operações
operacao_list = OperacaoListView.as_view()
operacao_create = OperacaoCreateView.as_view()
operacao_update = OperacaoUpdateView.as_view()
operacao_delete = OperacaoDeleteView.as_view()