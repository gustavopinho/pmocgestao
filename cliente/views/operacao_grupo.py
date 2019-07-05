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

from cliente.models import OperacaoGrupo
from core.utils import get_empresa


class OperacaoGrupoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = OperacaoGrupo
    paginate_by = 20
    raise_exception = True
    permission_required = (
        'cliente.view_operacaogrupo'
    )

    def get_queryset(self):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])
        
        try:
            q = self.request.GET.get("q")
            object_list = cliente.operacao_grupo.filter(nome__icontains=q)
        except:
            object_list = cliente.operacao_grupo.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(OperacaoGrupoListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q", '')
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        context['cliente'] = context['empresa'].clientes.get(pk=self.kwargs['cliente'])
        return context


class OperacaoGrupoCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = OperacaoGrupo
    fields = ['equipamento_grupo', 'codigo', 'nome']
    success_url = '/'
    success_message = 'Grupo de operações criado com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.add_operacaogrupo'
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        self.success_url = reverse_lazy(
            'empresa:cliente:operacao_grupo_list', 
            kwargs={"empresa" : empresa.pk, 'cliente' : cliente.pk}
        )
        
        form.instance.cliente = cliente
        return super(OperacaoGrupoCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(OperacaoGrupoCreateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        context['cliente'] = context['empresa'].clientes.get(pk=self.kwargs['cliente'])
        return context


class OperacaoGrupoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = OperacaoGrupo
    fields = ['equipamento_grupo', 'codigo', 'nome']
    template_name_suffix = '_form'
    success_url = '/'
    success_message = 'Grupo de operações atualizado com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.change_operacaogrupo',
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        self.success_url = reverse_lazy(
            'empresa:cliente:operacao_grupo_list', 
            kwargs={"empresa" : empresa.pk, 'cliente' : cliente.pk}
        )
        
        form.instance.cliente = cliente
        return super(OperacaoGrupoUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(OperacaoGrupoUpdateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        context['cliente'] = context['empresa'].clientes.get(pk=self.kwargs['cliente'])
        return context


class OperacaoGrupoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = OperacaoGrupo
    success_url = '/'
    success_message = 'Grupo de operações excluído com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.delete_operacaogrupo',
    )

    def get_object(self, queryset=None):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        self.success_url = reverse_lazy(
            'empresa:cliente:operacao_grupo_list', 
            kwargs={"empresa" : empresa.pk, 'cliente' : cliente.pk}
        )
        
        obj = cliente.operacao_grupo.get(pk=self.kwargs['pk'])
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(OperacaoGrupoDeleteView, self).delete(request, *args, **kwargs)

# Grupo de operações
operacao_grupo_list = OperacaoGrupoListView.as_view()
operacao_grupo_create = OperacaoGrupoCreateView.as_view()
operacao_grupo_update = OperacaoGrupoUpdateView.as_view()
operacao_grupo_delete = OperacaoGrupoDeleteView.as_view()
