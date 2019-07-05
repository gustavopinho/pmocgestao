import calendar

from datetime import date
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.edit import (
    CreateView, UpdateView
)
from django.urls import reverse_lazy

from cliente.models import Cliente
from core.utils import get_empresa

# Dashboard
class ClienteDashboardView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, View):
    template_name = 'cliente/dashboard.html'
    context = {}
    raise_exception = True
    permission_required = (
        'cliente.view_cliente'
    )

    def get(self, request, empresa, pk):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        self.context['cliente'] = empresa.clientes.get(pk=pk)

        return render(request, self.template_name, self.context)


class ClienteRelatoriosView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, View):
    raise_exception = True
    permission_required = (
        'cliente.view_cliente'
    )

    def get(self, request, empresa, pk):
        
        rel = request.GET.get('rel')
        ano = int(request.GET.get('ano'))

        empresa = get_empresa(self.request, self.kwargs['empresa'])
        cliente = empresa.clientes.get(pk=pk)

        # Relatório de manutenções mensal
        if rel == 'R1':

            data = {
                'labels': [
                    'Janeiro', 'Fevereiro', 'Março',
                    'Abril', 'Maio', 'Junho',
                    'Julho','Agosto', 'Setembro',
                    'Outubro', 'Novembro', 'Dezembro'
                ],
                'datasets' :[]
            }

            agendado = {
                'label': 'Agendado',
                'backgroundColor': '#E46651',
                'data' : []
            }

            executado = {
                'label': 'Executado',
                'backgroundColor': '#00D8FF',
                'data' : []
            }

            for m in range(1, 13):
                start_date = date(ano, m, 1)
                end_date = date(ano, m, calendar.monthrange(ano, m)[1])

                agendado['data'].append(cliente.manutencoes.filter(
                    data_prevista__range=(start_date, end_date),
                    tipo__nome='PREVENTIVA',
                    data_execucao__isnull=True
                ).count())

                executado['data'].append(cliente.manutencoes.filter(
                    data_prevista__range=(start_date, end_date),
                    tipo__nome='PREVENTIVA',
                    data_execucao__isnull=False
                ).count())

            data['datasets'].append(executado)
            data['datasets'].append(agendado)
            
            return JsonResponse({'results' : data})

        # Relatório de manutenções anual
        if rel == 'R2':

            start_date = date(ano, 1, 1)
            end_date = date(ano, 12, calendar.monthrange(ano, 12)[1])

            data = {
                'labels': ['Agendado', 'Executado'],
                'datasets' :[{
                    'backgroundColor': [
                        '#E46651',
                        '#00D8FF',
                    ],
                    'data': [
                        cliente.manutencoes.filter(
                            data_prevista__range=(start_date, end_date),
                            tipo__nome='PREVENTIVA',
                            data_execucao__isnull=True
                        ).count(),
                        cliente.manutencoes.filter(
                            data_prevista__range=(start_date, end_date),
                            tipo__nome='PREVENTIVA',
                            data_execucao__isnull=False
                        ).count(),
                    ]
                }]
            }

            return JsonResponse({'results' : data})


# Cliente
class ClienteCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Cliente
    fields = [
        'nome', 'razao_social', 'cnpj',
        'logradouro', 'numero', 'complemento',
        'bairro', 'cidade', 'uf', 'cep',
        'email', 'fone', 'celular', 'usuarios'
    ]
    success_url = '/'
    success_message = 'Cliente cadastrado com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.add_cliente'
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        self.success_url = reverse_lazy('core:dashboard')
        # Verificar se o usuário tem permissão para acessar essa empresa
        form.instance.empresa = empresa
        return super(ClienteCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ClienteCreateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        return context

    def get_form(self, form_class=None):    
        form = super(ClienteCreateView, self).get_form(form_class)
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        form.fields["usuarios"].queryset = empresa.usuarios.filter(acesso='PMOCCLIENTE', usuario__is_staff=False)
        return form


class ClienteUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Cliente
    fields = [
        'nome', 'razao_social', 'cnpj',
        'logradouro', 'numero', 'complemento',
        'bairro', 'cidade', 'uf', 'cep',
        'email', 'fone', 'celular', 'usuarios'
    ]
    success_url = '/'
    success_message = 'Cliente atualizado com sucesso!'
    raise_exception = True
    permission_required = (
        'cliente.change_cliente'
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        self.success_url = reverse_lazy('empresa:cliente:cliente_update', kwargs={"empresa" : empresa.pk, "pk": self.kwargs['pk']})
        # Verificar se o usuário tem permissão para acessar essa empresa
        form.instance.empresa = empresa
        return super(ClienteUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ClienteUpdateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        return context

    def get_form(self, form_class=None):    
        form = super(ClienteUpdateView, self).get_form(form_class)
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        form.fields["usuarios"].queryset = empresa.usuarios.filter(acesso='PMOCCLIENTE', usuario__is_staff=False)
        return form


# Cliente
cliente_dashboard = ClienteDashboardView.as_view()
cliente_relatorios = ClienteRelatoriosView.as_view()
cliente_create = ClienteCreateView.as_view()
cliente_update = ClienteUpdateView.as_view()