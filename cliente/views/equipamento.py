from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy

from cliente.models import Equipamento
from core.utils import get_empresa


class EquipamentoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Equipamento
    paginate_by = 50
    raise_exception = True
    permission_required = (
        'cliente.view_equipamento'
    )

    def get_queryset(self):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])
        # Verificar se o usuário tem permissão para acessar essa empresa
        try:
            q = self.request.GET.get("q")
            object_list = cliente.equipamentos.filter(nome__icontains=q)
        except:
            object_list = cliente.equipamentos.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(EquipamentoListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q", '')
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        context['cliente'] = context['empresa'].clientes.get(pk=self.kwargs['cliente'])
        return context


class EquipamentoDetailView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DetailView):
    model = Equipamento
    raise_exception = True
    permission_required = (
        'cliente.view_equipamento'
    )

    def get_object(self, queryset=None):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])
        obj = cliente.equipamentos.get(pk=self.kwargs['pk'])

        return obj


class EquipamentoCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Equipamento
    fields = [
        'ambiente', 'grupo', 'nome',
        'fabricante', 'identificacao', 'capacidade',
        'data_instalacao', 'ativo', 'data_desativado','observacao'
    ]
    success_url = '/'
    success_message = 'Equipamento criado com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.add_equipamento'
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        self.success_url = reverse_lazy(
            'empresa:cliente:equipamento_list',
            kwargs={"empresa" : empresa.pk, "cliente" : cliente.pk}
        )
        
        # Verificar se o usuário tem permissão para acessar essa empresa
        form.instance.cliente = cliente
        return super(EquipamentoCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EquipamentoCreateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        context['cliente'] = context['empresa'].clientes.get(pk=self.kwargs['cliente'])
        return context

    def get_form(self, form_class=None):    
        form = super(EquipamentoCreateView, self).get_form(form_class)
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        form.fields["grupo"].queryset = empresa.equipamento_grupos.all()
        form.fields["ambiente"].queryset = cliente.ambientes.all()
        return form


class EquipamentoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Equipamento
    fields = [
        'ambiente', 'grupo', 'nome',
        'fabricante', 'identificacao', 'capacidade',
        'data_instalacao', 'ativo', 'data_desativado', 'observacao'
    ]
    template_name_suffix = '_form'
    success_url = '/'
    success_message = 'Equipamento atualizado com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.change_equipamento',
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        self.success_url = reverse_lazy(
            'empresa:cliente:equipamento_list',
            kwargs={"empresa" : empresa.pk, "cliente" : cliente.pk}
        )
        
        # Verificar se o usuário tem permissão para acessar essa empresa
        form.instance.cliente = cliente
        return super(EquipamentoUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EquipamentoUpdateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        context['cliente'] = context['empresa'].clientes.get(pk=self.kwargs['cliente'])
        return context

    def get_form(self, form_class=None):    
        form = super(EquipamentoUpdateView, self).get_form(form_class)
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        form.fields["grupo"].queryset = empresa.equipamento_grupos.all()
        form.fields["ambiente"].queryset = cliente.ambientes.all()
        return form


class EquipamentoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Equipamento
    success_url = '/'
    success_message = 'Equipamento excluído com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.delete_equipamento',
    )

    def get_object(self, queryset=None):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        self.success_url = reverse_lazy(
            'empresa:cliente:equipamento_list',
            kwargs={"empresa" : empresa.pk, "cliente" : cliente.pk}
        )
        
        obj = cliente.equipamentos.get(pk=self.kwargs['pk'])
        return obj

    def delete(self, request, *args, **kwargs):
        
        try:
            r = super(EquipamentoDeleteView, self).delete(request, *args, **kwargs)
            messages.success(self.request, self.success_message)
            return r
        except IntegrityError as e:
            messages.error(self.request, 'Você não pode excluír esse equipamento, existem manutenções cadastradas para ele!')
        return HttpResponseRedirect(self.success_url)


# Equipamento
equipamento_list = EquipamentoListView.as_view()
equipamento_create = EquipamentoCreateView.as_view()
equipamento_detail = EquipamentoDetailView.as_view()
equipamento_update = EquipamentoUpdateView.as_view()
equipamento_delete = EquipamentoDeleteView.as_view()