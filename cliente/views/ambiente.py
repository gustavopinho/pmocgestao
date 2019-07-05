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

from cliente.models import Ambiente
from core.utils import get_empresa

class AmbienteListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Ambiente
    paginate_by = 20
    raise_exception = True
    permission_required = (
        'cliente.view_ambiente'
    )

    def get_queryset(self):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])
        # Verificar se o usuário tem permissão para acessar essa empresa
        try:
            q = self.request.GET.get("q")
            object_list = cliente.ambientes.filter(nome__icontains=q)
        except:
            object_list = cliente.ambientes.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(AmbienteListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q", '')
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        context['cliente'] = context['empresa'].clientes.get(pk=self.kwargs['cliente'])
        return context


class AmbienteCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Ambiente
    fields = [
        'unidade', 'atividade', 'nome',
        'identificacao', 'ocupantes', 'area',
        'carga_termica'
    ]
    success_url = '/'
    success_message = 'Ambiente criado com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.add_ambiente'
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        self.success_url = reverse_lazy(
            'empresa:cliente:ambiente_list',
            kwargs={"empresa" : empresa.pk, "cliente" : cliente.pk}
        )
        
        # Verificar se o usuário tem permissão para acessar essa empresa
        form.instance.cliente = cliente
        return super(AmbienteCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AmbienteCreateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        context['cliente'] = context['empresa'].clientes.get(pk=self.kwargs['cliente'])
        return context

    def get_form(self, form_class=None):    
        form = super(AmbienteCreateView, self).get_form(form_class)
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        form.fields["unidade"].queryset = cliente.unidades.all()
        form.fields["atividade"].queryset = cliente.atividades.all()
        return form


class AmbienteUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Ambiente
    fields = [
        'unidade', 'atividade', 'nome',
        'identificacao', 'ocupantes', 'area',
        'carga_termica'
    ]
    template_name_suffix = '_form'
    success_url = '/'
    success_message = 'Ambiente atualizado com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.change_ambiente',
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        self.success_url = reverse_lazy(
            'empresa:cliente:ambiente_list',
            kwargs={"empresa" : empresa.pk, "cliente" : cliente.pk}
        )
        
        # Verificar se o usuário tem permissão para acessar essa empresa
        form.instance.cliente = cliente
        return super(AmbienteUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AmbienteUpdateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        context['cliente'] = context['empresa'].clientes.get(pk=self.kwargs['cliente'])
        return context

    def get_form(self, form_class=None):    
        form = super(AmbienteUpdateView, self).get_form(form_class)
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        form.fields["unidade"].queryset = cliente.unidades.all()
        form.fields["atividade"].queryset = cliente.atividades.all()
        return form


class AmbienteDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Ambiente
    success_url = '/'
    success_message = 'Ambiente excluído com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.delete_ambiente',
    )

    def get_object(self, queryset=None):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        self.success_url = reverse_lazy(
            'empresa:cliente:ambiente_list',
            kwargs={"empresa" : empresa.pk, "cliente" : cliente.pk}
        )
        
        obj = cliente.ambientes.get(pk=self.kwargs['pk'])
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(AmbienteDeleteView, self).delete(request, *args, **kwargs)

# Ambiente
ambiente_list = AmbienteListView.as_view()
ambiente_create = AmbienteCreateView.as_view()
ambiente_update = AmbienteUpdateView.as_view()
ambiente_delete = AmbienteDeleteView.as_view()
