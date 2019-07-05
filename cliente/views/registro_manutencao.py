import functools
import operator

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
from django.utils import timezone
from django.db.models import Q

from cliente.models import RegistroManutencao
from cliente.forms import RegistroManutencaoFilter
from core.utils import get_empresa


class RegistroManutencaoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = RegistroManutencao
    paginate_by = 20
    raise_exception = True
    permission_required = (
        'cliente.view_registromanutencao'
    )

    def get_queryset(self):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])
        
        try:
            form = RegistroManutencaoFilter(cliente, self.request.GET)

            object_list = cliente.manutencoes.all()
            if form.is_valid():            

                filter_clauses = []

                if form.cleaned_data['unidade']:
                    filter_clauses.append(Q(equipamento__ambiente__unidade__in=form.cleaned_data['unidade']))

                if form.cleaned_data['tipo']:
                    filter_clauses.append(Q(tipo__id__in=form.cleaned_data['tipo']))

                if form.cleaned_data['equipamentos']:
                    filter_clauses.append(Q(equipamento__in=form.cleaned_data['equipamentos']))

                if form.cleaned_data['executado']:
                    if form.cleaned_data['executado'] == '2':
                        filter_clauses.append(Q(data_execucao__isnull=True))
                    else:
                        filter_clauses.append(Q(data_execucao__isnull=False))

                if form.cleaned_data['date_start']:
                    filter_clauses.append(Q(data_prevista__gte=form.cleaned_data['date_start']))

                if form.cleaned_data['date_start']:
                    filter_clauses.append(Q(data_prevista__lte=form.cleaned_data['date_end']))

                if filter_clauses:
                    object_list = object_list.filter(functools.reduce(operator.and_, filter_clauses))
        
        except Exception as e:
            raise(e)

        return object_list

    def get_context_data(self, **kwargs):
        context = super(RegistroManutencaoListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q", '')
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        context['cliente'] = context['empresa'].clientes.get(pk=self.kwargs['cliente'])
        context['form'] = RegistroManutencaoFilter(context['cliente'], self.request.GET)
        return context


class RegistroManutencaoDetailView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DetailView):
    model = RegistroManutencao
    raise_exception = True
    permission_required = (
        'cliente.view_registromanutencao'
    )

    def get_object(self, queryset=None):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])
        obj = cliente.manutencoes.get(pk=self.kwargs['pk'])

        return obj


class RegistroManutencaoCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = RegistroManutencao
    fields = [
        'equipamento', 'tecnico', 'tipo',
        'data_prevista', 'data_execucao', 'observacao'
    ]
    success_url = '/'
    success_message = 'Registro de manutenção criado com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.add_registromanutencao',
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        self.success_url = reverse_lazy(
            'empresa:cliente:registro_manutencao_list',
            kwargs={"empresa" : empresa.pk, "cliente" : cliente.pk}
        )
        
        # Verificar se o usuário tem permissão para acessar essa empresa
        form.instance.cliente = cliente
        self.object = form.save()

        self.success_url = reverse_lazy(
            'empresa:cliente:registro_manutencao_update',
            kwargs={"empresa" : empresa.pk, "cliente" : cliente.pk, 'pk' : self.object.pk }
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RegistroManutencaoCreateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        context['cliente'] = context['empresa'].clientes.get(pk=self.kwargs['cliente'])
        return context

    def get_form(self, form_class=None):    
        form = super(RegistroManutencaoCreateView, self).get_form(form_class)
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        form.fields["tipo"].queryset = empresa.manutencao_tipo.all()
        form.fields["tecnico"].queryset = empresa.tecnicos.all()
        form.fields["equipamento"].queryset = cliente.equipamentos.all()
        return form


class RegistroManutencaoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = RegistroManutencao
    fields = [
        'equipamento', 'tecnico', 'tipo',
        'data_prevista', 'data_execucao', 'observacao'
    ]
    template_name = 'cliente/registromanutencao_update_form.html'
    success_url = '/'
    success_message = 'Registro de manutenção atualizado com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.change_registromanutencao',
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        self.success_url = reverse_lazy(
            'empresa:cliente:registro_manutencao_update',
            kwargs={"empresa" : empresa.pk, "cliente" : cliente.pk, 'pk':self.kwargs['pk']}
        )
        
        # Verificar se o usuário tem permissão para acessar essa empresa
        form.instance.cliente = cliente
        return super(RegistroManutencaoUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RegistroManutencaoUpdateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        context['cliente'] = context['empresa'].clientes.get(pk=self.kwargs['cliente'])
        return context

    def get_form(self, form_class=None):    
        form = super(RegistroManutencaoUpdateView, self).get_form(form_class)
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        form.fields["tipo"].queryset = empresa.manutencao_tipo.all()
        form.fields["tecnico"].queryset = empresa.tecnicos.all()
        form.fields["equipamento"].queryset = cliente.equipamentos.all()
        return form


class RegistroManutencaoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = RegistroManutencao
    success_url = '/'
    success_message = 'Registro de Manutenção excluído com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.delete_registromanutencao',
    )

    def get_object(self, queryset=None):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=self.kwargs['cliente'])

        self.success_url = reverse_lazy(
            'empresa:cliente:registro_manutencao_list',
            kwargs={"empresa" : empresa.pk, "cliente" : cliente.pk}
        )
        
        obj = cliente.manutencoes.get(pk=self.kwargs['pk'])
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(RegistroManutencaoDeleteView, self).delete(request, *args, **kwargs)

# Registro de Manutenção
registro_manutencao_list = RegistroManutencaoListView.as_view()
registro_manutencao_create = RegistroManutencaoCreateView.as_view()
registro_manutencao_detail = RegistroManutencaoDetailView.as_view()
registro_manutencao_update = RegistroManutencaoUpdateView.as_view()
registro_manutencao_delete = RegistroManutencaoDeleteView.as_view()