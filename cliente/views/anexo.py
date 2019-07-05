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

from cliente.models import Anexo
from core.utils import get_empresa

class AnexoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Anexo
    paginate_by = 20
    raise_exception = True
    permission_required = (
        'cliente.view_anexo'
    )

    def get_queryset(self):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        try:
            q = self.request.GET.get("q")
            object_list = cliente.anexos.filter(nome__icontains=q)
        except:
            object_list = cliente.anexos.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(AnexoListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q", '')
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        context['cliente'] = empresa.clientes.get(pk=self.kwargs['cliente'])
        return context


class AnexoCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Anexo
    fields = ['anexo', 'nome']
    success_url = '/'
    success_message = 'Anexo criado com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.add_anexo'
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        self.success_url = reverse_lazy(
            'empresa:cliente:anexo_list',
            kwargs={"empresa" : empresa.pk, 'cliente' : cliente.pk}
        )
        
        form.instance.cliente = cliente
        return super(AnexoCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AnexoCreateView, self).get_context_data(**kwargs)
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        context['cliente'] = empresa.clientes.get(pk=self.kwargs['cliente'])
        return context


class AnexoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Anexo
    fields = ['anexo', 'nome']
    template_name_suffix = '_form'
    success_url = '/'
    success_message = 'Anexo atualizado com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.change_anexo',
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        self.success_url = reverse_lazy(
            'empresa:cliente:anexo_list',
            kwargs={"empresa" : empresa.pk, 'cliente' : cliente.pk}
        )
        
        form.instance.cliente = cliente
        return super(AnexoUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AnexoUpdateView, self).get_context_data(**kwargs)
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        context['cliente'] = empresa.clientes.get(pk=self.kwargs['cliente'])
        return context


class AnexoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Anexo
    success_url = '/'
    success_message = 'Anexo excluído com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.delete_anexo',
    )

    def get_object(self, queryset=None):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        self.success_url = reverse_lazy(
            'empresa:cliente:anexo_list',
            kwargs={"empresa" : empresa.pk, 'cliente' : cliente.pk}
        )
        
        obj = cliente.anexos.get(pk=self.kwargs['pk'])
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(AnexoDeleteView, self).delete(request, *args, **kwargs)


# Anexo
anexo_list = AnexoListView.as_view()
anexo_create = AnexoCreateView.as_view()
anexo_update = AnexoUpdateView.as_view()
anexo_delete = AnexoDeleteView.as_view()