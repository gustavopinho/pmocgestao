import functools
import operator
import calendar

from datetime import date
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView, FormView
)

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm

from .models import (
    Empresa, UsuarioEmpresa, EquipamentoGrupo,
    ManutencaoTipo, ManutencaoIntervalo, Responsavel,
    Tecnico, UsuarioEmpresa
)
from .forms import EmpresaForm, UsuarioEmpresaForm
from accounts.models import User
from accounts.forms import UserAdminForm, UserRegisterForm

from core.utils import get_empresa


class EmpresaDashboardView(LoginRequiredMixin, PermissionRequiredMixin, View):
    model = Empresa
    form = EmpresaForm
    context = {}
    template_name = 'empresa/dashboard.html'
    raise_exception = True
    permission_required = (
        'empresa.view_empresa',
    )

    def get(self, request, pk):

        self.context['empresa'] = get_empresa(request, pk)
        return render(request, self.template_name, self.context)


class EmpresaRelatoriosView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, View):
    raise_exception = True
    permission_required = (
        'empresa.view_empresa'
    )

    def get(self, request, pk):
        
        rel = request.GET.get('rel')
        ano = int(request.GET.get('ano'))

        empresa = get_empresa(self.request, pk)
        
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

                _agendado = 0;
                _executado = 0;

                for cliente in empresa.clientes.all():
                    _agendado += cliente.manutencoes.filter(
                        data_prevista__range=(start_date, end_date),
                        tipo__nome='PREVENTIVA',
                        data_execucao__isnull=True
                    ).count()

                    _executado += cliente.manutencoes.filter(
                        data_prevista__range=(start_date, end_date),
                        tipo__nome='PREVENTIVA',
                        data_execucao__isnull=False
                    ).count()

                agendado['data'].append(_agendado)
                executado['data'].append(_executado)

            data['datasets'].append(executado)
            data['datasets'].append(agendado)
            
            return JsonResponse({'results' : data})

        # Relatório de manutenções anual
        if rel == 'R2':

            start_date = date(ano, 1, 1)
            end_date = date(ano, 12, calendar.monthrange(ano, 12)[1])

            _agendado = 0;
            _executado = 0;

            for cliente in empresa.clientes.all():
                _agendado += cliente.manutencoes.filter(
                    data_prevista__range=(start_date, end_date),
                    tipo__nome='PREVENTIVA',
                    data_execucao__isnull=True
                ).count()

                _executado += cliente.manutencoes.filter(
                    data_prevista__range=(start_date, end_date),
                    tipo__nome='PREVENTIVA',
                    data_execucao__isnull=False
                ).count()



            data = {
                'labels': ['Agendado', 'Executado'],
                'datasets' :[{
                    'backgroundColor': [
                        '#E46651',
                        '#00D8FF',
                    ],
                    'data': [_agendado, _executado]
                }]
            }

            return JsonResponse({'results' : data})


class EmpresaCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Empresa
    fields = [
        'nome', 'razao_social', 'cnpj', 
        'logradouro', 'numero', 'complemento',
        'bairro', 'cidade', 'uf', 'cep', 'email',
        'fone', 'logo'
    ]
    success_url = '/'
    success_message = 'Empresa criada com sucesso!'
    raise_exception = True
    permission_required = (
        'empresa.add_empresa'
    )

    def form_valid(self, form):
        empresa = form.save()
        
        usuario_empresa = UsuarioEmpresa(usuario=self.request.user, empresa=empresa)
        usuario_empresa.save()

        self.success_url = reverse_lazy('empresa:empresa_update', kwargs={"pk" : empresa.pk })
        
        return super(EmpresaCreateView, self).form_valid(form)


class EmpresaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Empresa
    fields = [
        'nome', 'razao_social', 'cnpj', 
        'logradouro', 'numero', 'complemento',
        'bairro', 'cidade', 'uf', 'cep', 'email',
        'fone', 'logo'
    ]
    template_name_suffix = '_form'
    success_url = '/'
    success_message = 'Empresa atualizada com sucesso!'
    raise_exception = True
    permission_required = (
        'empresa.change_empresa',
    )

    def form_valid(self, form):
        self.success_url = reverse_lazy('empresa:empresa_update', kwargs={"pk" : self.kwargs['pk'] })
        return super(EmpresaUpdateView, self).form_valid(form)


# Equipamento Grupo
class EquipamentoGrupoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = EquipamentoGrupo
    paginate_by = 20
    raise_exception = True
    permission_required = (
        'empresa.view_equipamentogrupo'
    )

    def get_queryset(self):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        # Verificar se o usuário tem permissão para acessar essa empresa
        try:
            q = self.request.GET.get("q")
            object_list = empresa.equipamento_grupos.filter(nome__icontains=q)
        except:
            object_list = empresa.equipamento_grupos.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(EquipamentoGrupoListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q", '')
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        return context


class EquipamentoGrupoCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = EquipamentoGrupo
    fields = ['nome']
    success_url = '/'
    success_message = 'Grupo de equipamento criado com sucesso!'
    raise_exception = True
    permission_required = (
        'empresa.add_equipamentogrupo'
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        self.success_url = reverse_lazy('empresa:equipamento_grupo_list', kwargs={"empresa" : empresa.pk })
        # Verificar se o usuário tem permissão para acessar essa empresa
        form.instance.empresa = empresa
        return super(EquipamentoGrupoCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EquipamentoGrupoCreateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        return context


class EquipamentoGrupoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = EquipamentoGrupo
    fields = ['nome']
    template_name_suffix = '_form'
    success_url = '/'
    success_message = 'Grupo de equipamento atualizado com sucesso!'
    raise_exception = True
    permission_required = (
        'empresa.change_equipamentogrupo',
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        self.success_url = reverse_lazy('empresa:equipamento_grupo_list', kwargs={"empresa" : empresa.pk })
        # Verificar se o usuário tem permissão para acessar essa empresa
        form.instance.empresa = empresa
        return super(EquipamentoGrupoUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EquipamentoGrupoUpdateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        return context


class EquipamentoGrupoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = EquipamentoGrupo
    success_url = '/'
    success_message = 'Grupo de equipamentos excluído com sucesso!'
    raise_exception = True
    permission_required = (
        'empresa.delete_equipamentogrupo',
    )

    def get_object(self, queryset=None):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        self.success_url = reverse_lazy('empresa:equipamento_grupo_list', kwargs={"empresa" : empresa.pk })
        obj = empresa.equipamento_grupos.get(pk=self.kwargs['pk'])

        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(EquipamentoGrupoDeleteView, self).delete(request, *args, **kwargs)


# Tipo de Manutenção
class ManutencaoTipoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ManutencaoTipo
    paginate_by = 20
    raise_exception = True
    permission_required = (
        'empresa.view_manutencaotipo'
    )

    def get_queryset(self):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        # Verificar se o usuário tem permissão para acessar essa empresa
        try:
            q = self.request.GET.get("q")
            object_list = empresa.manutencao_tipo.filter(nome__icontains=q)
        except:
            object_list = empresa.manutencao_tipo.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(ManutencaoTipoListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q", '')
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        return context


class ManutencaoTipoCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ManutencaoTipo
    fields = ['nome']
    success_url = '/'
    success_message = 'Tipo de manutenção criado com sucesso!'
    raise_exception = True
    permission_required = (
        'empresa.add_manutencaotipo'
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        self.success_url = reverse_lazy('empresa:manutencao_tipo_list', kwargs={"empresa" : empresa.pk })
        # Verificar se o usuário tem permissão para acessar essa empresa
        form.instance.empresa = empresa
        return super(ManutencaoTipoCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ManutencaoTipoCreateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        return context


class ManutencaoTipoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ManutencaoTipo
    fields = ['nome']
    template_name_suffix = '_form'
    success_url = '/'
    success_message = 'Tipo de manutenção atualizado com sucesso!'
    raise_exception = True
    permission_required = (
        'empresa.change_manutencaotipo',
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        self.success_url = reverse_lazy('empresa:manutencao_tipo_list', kwargs={"empresa" : empresa.pk })
        # Verificar se o usuário tem permissão para acessar essa empresa
        form.instance.empresa = empresa
        return super(ManutencaoTipoUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ManutencaoTipoUpdateView, self).get_context_data(**kwargs)
        context['empresa'] =get_empresa(self.request, self.kwargs['empresa'])
        return context


class ManutencaoTipoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ManutencaoTipo
    success_url = '/'
    success_message = 'Tipo de manutenção excluído com sucesso!'
    raise_exception = True
    permission_required = (
        'empresa.delete_manutencaotipo',
    )

    def get_object(self, queryset=None):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        self.success_url = reverse_lazy('empresa:manutencao_tipo_list', kwargs={"empresa" : empresa.pk })
        obj = empresa.manutencao_tipo.get(pk=self.kwargs['pk'])

        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ManutencaoTipoDeleteView, self).delete(request, *args, **kwargs)


# Intervalo de Manutenções
class ManutencaoIntervaloListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ManutencaoIntervalo
    paginate_by = 20
    raise_exception = True
    permission_required = (
        'empresa.view_manutencaointervalo'
    )

    def get_queryset(self):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        # Verificar se o usuário tem permissão para acessar essa empresa
        try:
            q = self.request.GET.get("q")
            object_list = empresa.manutencao_intervalo.filter(nome__icontains=q)
        except:
            object_list = empresa.manutencao_intervalo.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(ManutencaoIntervaloListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q", '')
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        return context


class ManutencaoIntervaloCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ManutencaoIntervalo
    fields = ['nome', 'dias']
    success_url = '/'
    success_message = 'Intervalo de manutenção criado com sucesso!'
    raise_exception = True
    permission_required = (
        'empresa.add_manutencaointervalo'
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        self.success_url = reverse_lazy('empresa:manutencao_intervalo_list', kwargs={"empresa" : empresa.pk })
        # Verificar se o usuário tem permissão para acessar essa empresa
        form.instance.empresa = empresa
        return super(ManutencaoIntervaloCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ManutencaoIntervaloCreateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        return context


class ManutencaoIntervaloUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ManutencaoIntervalo
    fields = ['nome', 'dias']
    template_name_suffix = '_form'
    success_url = '/'
    success_message = 'Intervalo de manutenção atualizado com sucesso!'
    raise_exception = True
    permission_required = (
        'empresa.change_manutencaointervalo',
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        self.success_url = reverse_lazy('empresa:manutencao_intervalo_list', kwargs={"empresa" : empresa.pk })
        # Verificar se o usuário tem permissão para acessar essa empresa
        form.instance.empresa = empresa
        return super(ManutencaoIntervaloUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ManutencaoIntervaloUpdateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        return context


class ManutencaoIntervaloDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ManutencaoIntervalo
    success_url = '/'
    success_message = 'Intervalo de manutenção excluído com sucesso!'
    raise_exception = True
    permission_required = (
        'empresa.delete_manutencaointervalo',
    )

    def get_object(self, queryset=None):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        self.success_url = reverse_lazy('empresa:manutencao_intervalo_list', kwargs={"empresa" : empresa.pk })
        obj = empresa.manutencao_intervalo.get(pk=self.kwargs['pk'])

        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ManutencaoIntervaloDeleteView, self).delete(request, *args, **kwargs)


# Resposável Técnico
class ResponsavelListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Responsavel
    paginate_by = 20
    raise_exception = True
    permission_required = (
        'empresa.view_responsavel'
    )

    def get_queryset(self):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        # Verificar se o usuário tem permissão para acessar essa empresa
        try:
            q = self.request.GET.get("q")
            object_list = empresa.responsaveis.filter(nome__icontains=q)
        except:
            object_list = empresa.responsaveis.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(ResponsavelListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q", '')
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        return context


class ResponsavelCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Responsavel
    fields = [
        'nome', 'cnpj', 
        'logradouro', 'numero', 'complemento',
        'bairro', 'cidade', 'uf', 'cep', 'email',
        'fone', 'registro_conselho'
    ]
    success_url = '/'
    success_message = 'Responsável técnico criado com sucesso!'
    raise_exception = True
    permission_required = (
        'empresa.add_responsavel'
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        self.success_url = reverse_lazy('empresa:responsavel_list', kwargs={"empresa" : empresa.pk })
        # Verificar se o usuário tem permissão para acessar essa empresa
        form.instance.empresa = empresa
        return super(ResponsavelCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ResponsavelCreateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        return context


class ResponsavelUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Responsavel
    fields = [
        'nome', 'cnpj', 
        'logradouro', 'numero', 'complemento',
        'bairro', 'cidade', 'uf', 'cep', 'email',
        'fone', 'registro_conselho'
    ]
    template_name_suffix = '_form'
    success_url = '/'
    success_message = 'Responsável técnico atualizado com sucesso!'
    raise_exception = True
    permission_required = (
        'empresa.change_responsavel',
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        self.success_url = reverse_lazy('empresa:responsavel_list', kwargs={"empresa" : empresa.pk })
        # Verificar se o usuário tem permissão para acessar essa empresa
        form.instance.empresa = empresa
        return super(ResponsavelUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ResponsavelUpdateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        return context


class ResponsavelDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Responsavel
    success_url = '/'
    success_message = 'Responsável técnico excluído com sucesso!'
    raise_exception = True
    permission_required = (
        'empresa.delete_responsavel',
    )

    def get_object(self, queryset=None):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        self.success_url = reverse_lazy('empresa:responsavel_list', kwargs={"empresa" : empresa.pk })
        obj = empresa.responsaveis.get(pk=self.kwargs['pk'])

        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ResponsavelDeleteView, self).delete(request, *args, **kwargs)


# Resposável Técnico
class TecnicoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Tecnico
    paginate_by = 20
    raise_exception = True
    permission_required = (
        'empresa.view_tecnico'
    )

    def get_queryset(self):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        try:
            q = self.request.GET.get("q")
            object_list = empresa.tecnicos.filter(nome__icontains=q)
        except:
            object_list = empresa.tecnicos.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(TecnicoListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q", '')
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        return context


class TecnicoCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tecnico
    fields = [
        'nome', 'logradouro', 'numero',
        'complemento', 'bairro', 'cidade',
        'uf', 'cep', 'email', 'fone',
    ]
    success_url = '/'
    success_message = 'Técnico criado com sucesso!'
    raise_exception = True
    permission_required = (
        'empresa.add_tecnico'
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        self.success_url = reverse_lazy('empresa:tecnico_list', kwargs={"empresa" : empresa.pk })
        # Verificar se o usuário tem permissão para acessar essa empresa
        form.instance.empresa = empresa
        return super(TecnicoCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TecnicoCreateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        return context


class TecnicoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tecnico
    fields = [
        'nome', 'logradouro', 'numero',
        'complemento', 'bairro', 'cidade',
        'uf', 'cep', 'email', 'fone',
    ]
    template_name_suffix = '_form'
    success_url = '/'
    success_message = 'Técnico atualizado com sucesso!'
    raise_exception = True
    permission_required = (
        'empresa.change_tecnico',
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        self.success_url = reverse_lazy('empresa:tecnico_list', kwargs={"empresa" : empresa.pk })
        # Verificar se o usuário tem permissão para acessar essa empresa
        form.instance.empresa = empresa
        return super(TecnicoUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TecnicoUpdateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        return context


class TecnicoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Tecnico
    success_url = '/'
    success_message = 'Técnico excluído com sucesso!'
    raise_exception = True
    permission_required = (
        'empresa.delete_tecnico',
    )

    def get_object(self, queryset=None):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        self.success_url = reverse_lazy('empresa:tecnico_list', kwargs={"empresa" : empresa.pk })
        obj = empresa.tecnicos.get(pk=self.kwargs['pk'])

        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(TecnicoDeleteView, self).delete(request, *args, **kwargs)


# Usuários
class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = "empresa/user_list.html"
    paginate_by = 20
    raise_exception = True
    permission_required = (
        'accounts.view_userempresa'
    )

    def get_queryset(self):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        # Verificar se o usuário tem permissão para acessar essa empresa
        try:
            q = self.request.GET.get("q")
            object_list = empresa.usuarios.filter(usuario__nome__icontains=q, usuario__is_staff=False)
        except:
            object_list = empresa.usuarios.filter(usuario__is_staff=False)
        return object_list

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q", '')
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        return context


class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "empresa/user_form.html"
    success_url = '/'
    success_message = 'Usuário criado com sucesso!'
    raise_exception = True
    permission_required = (
        'accounts.add_userempresa'
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        self.success_url = reverse_lazy('empresa:user_list', kwargs={"empresa" : empresa.pk })
        # Verificar se o usuário tem permissão para acessar essa empresa

        self.object = form.save()
        # Vincular o usuário à empresa
        usuario_empresa = UsuarioEmpresa(usuario=self.object, empresa=empresa)
        usuario_empresa.save()
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        return context


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ['name', 'email', 'is_active']
    template_name = "empresa/user_update_form.html"
    template_name_suffix = '_form'
    success_url = '/'
    success_message = 'Usuário atualizado com sucesso!'
    raise_exception = True
    permission_required = (
        'accounts.change_userempresa',
    )

    def form_valid(self, form):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        self.success_url = reverse_lazy('empresa:user_list', kwargs={"empresa" : empresa.pk })
        # Verificar se o usuário tem permissão para acessar essa empresa
        
        self.object = form.save()
        if self.object == self.request.user and self.object.is_active is False:
            self.object.is_active = True
            self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        return context


class UserDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_url = '/'
    template_name = "empresa/user_confirm_delete.html"
    success_message = 'Usuário excluído com sucesso!'
    raise_exception = True
    permission_required = (
        'accounts.delete_userempresa',
    )

    def get_object(self, queryset=None):
        empresa = get_empresa(self.request, self.kwargs['empresa'])
        self.success_url = reverse_lazy('empresa:user_list', kwargs={"empresa" : empresa.pk })

        obj = User.objects.get(pk=self.kwargs['pk'], is_staff=False)

        try:
            usuario_empresa = empresa.usuarios.get(usuario=obj.pk, usuario__is_staff=False)
            return usuario_empresa.usuario
        except:
            return None

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object == self.request.user:
            messages.error(self.request, 'Não é possível excluír o usuário, ele está sendo usado por você.')
            success_url = self.get_success_url()
            return HttpResponseRedirect(success_url)
        else:
            messages.success(self.request, self.success_message)
            return super(UserDeleteView, self).delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserDeleteView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        return context


class UserUpdatePasswordView(LoginRequiredMixin, PermissionRequiredMixin,SuccessMessageMixin, FormView):

    template_name = 'empresa/user_update_password.html'
    success_url = '/'
    form_class = SetPasswordForm
    success_message = 'Senha alterada com sucesso!'
    raise_exception = True
    permission_required = (
        'accounts.change_userempresa',
    )

    def get_form_kwargs(self):
        kwargs = super(UserUpdatePasswordView, self).get_form_kwargs()

        empresa = get_empresa(self.request, self.kwargs['empresa'])
        self.success_url = reverse_lazy('empresa:user_list', kwargs={"empresa" : empresa.pk })
        usuario_empresa = empresa.usuarios.get(usuario=self.kwargs['pk'], usuario__is_staff=False)
        kwargs['user'] = usuario_empresa.usuario
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(UserUpdatePasswordView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UserUpdatePasswordView, self).get_context_data(**kwargs)
        context['empresa'] = get_empresa(self.request, self.kwargs['empresa'])
        return context


# Gerar acesso
class UserGerarAcessoView(LoginRequiredMixin, PermissionRequiredMixin, View):
    context = {}
    template_name = 'empresa/gerar_acesso.html'
    raise_exception = True
    permission_required = (
        'empresa.change_empresa',
        'accounts.change_userempresa',
    )

    def get(self, request, empresa, usuario):
        empresa = get_empresa(self.request, empresa)
        usuario_empresa = empresa.usuarios.get(usuario=usuario, usuario__is_staff=False)
        usuario = usuario_empresa.usuario

        self.context['empresa'] = empresa
        self.context['usuario'] = usuario
        self.context['form'] = UsuarioEmpresaForm(instance=usuario_empresa)
        
        return render(request, self.template_name, self.context)

    
    def post(self, request, empresa, usuario):
        empresa = get_empresa(self.request, empresa)
        usuario_empresa = empresa.usuarios.get(usuario=usuario, usuario__is_staff=False)

        self.context['empresa'] = empresa
        self.context['usuario'] = usuario
        
        form = UsuarioEmpresaForm(request.POST, instance=usuario_empresa)

        if form.is_valid():
            form.save()
            messages.success(request, 'Operação realizada com sucesso!')
            return HttpResponseRedirect(reverse('empresa:user_list', kwargs={'empresa':empresa.pk}))
        
        return render(request, self.template_name, self.context)

        

# Dashboard
empresa_dashboard = EmpresaDashboardView.as_view()
empresa_relatorios =   EmpresaRelatoriosView.as_view()

# Empresa
empresa_create = EmpresaCreateView.as_view()
empresa_update = EmpresaUpdateView.as_view()

# Equipamento Grupo
equipamento_grupo_list = EquipamentoGrupoListView.as_view()
equipamento_grupo_create = EquipamentoGrupoCreateView.as_view()
equipamento_grupo_update = EquipamentoGrupoUpdateView.as_view()
equipamento_grupo_delete = EquipamentoGrupoDeleteView.as_view()

# Tipo de Manutenção
manutencao_tipo_list = ManutencaoTipoListView.as_view()
manutencao_tipo_create = ManutencaoTipoCreateView.as_view()
manutencao_tipo_update = ManutencaoTipoUpdateView.as_view()
manutencao_tipo_delete = ManutencaoTipoDeleteView.as_view()

# Intervalo de Manutenção
manutencao_intervalo_list = ManutencaoIntervaloListView.as_view()
manutencao_intervalo_create = ManutencaoIntervaloCreateView.as_view()
manutencao_intervalo_update = ManutencaoIntervaloUpdateView.as_view()
manutencao_intervalo_delete = ManutencaoIntervaloDeleteView.as_view()

# Responsável
responsavel_list = ResponsavelListView.as_view()
responsavel_create = ResponsavelCreateView.as_view()
responsavel_update = ResponsavelUpdateView.as_view()
responsavel_delete = ResponsavelDeleteView.as_view()

# Técnicos
tecnico_list = TecnicoListView.as_view()
tecnico_create = TecnicoCreateView.as_view()
tecnico_update = TecnicoUpdateView.as_view()
tecnico_delete = TecnicoDeleteView.as_view()

# Usuários
user_list = UserListView.as_view()
user_create = UserCreateView.as_view()
user_update = UserUpdateView.as_view()
user_update_password = UserUpdatePasswordView.as_view()
user_delete = UserDeleteView.as_view()
user_gerar_acesso = UserGerarAcessoView.as_view()