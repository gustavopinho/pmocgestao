import functools
import operator
import calendar

from datetime import date

from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView, FormView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.contrib import messages

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.utils import timezone
from django.db.models import Q

from empresa.models import (
    Empresa
)
from .models import (
    Cliente, Unidade, Atividade,
    Ambiente, Equipamento, RegistroManutencao,
    OperacaoGrupo, Operacao, RegistroManutencaoOperacao,
    Anexo
)

from .forms import (
    MedicoesForm, RegistroManutencaoFilter, ,
    RegistroManutencaoAnexoForm
)
from core.utils import get_empresa


# Equipamento Anexos



# Anexo



# Relatórios



# Ferramentas
class FerramentasView(LoginRequiredMixin, PermissionRequiredMixin, View):
    template_name = 'cliente/ferramentas.html'
    context = {}
    raise_exception = True
    permission_required = (
        'cliente.add_registromanutencao',
    )

    def get(self, request, empresa, cliente):
        self.context['empresa'] = get_empresa(request, empresa)
        self.context['cliente'] = self.context['empresa'].clientes.get(pk=cliente)
        self.context['equipamentos'] = self.context['cliente'].equipamentos.all()

        return render(request, self.template_name, self.context)


class FerramentaGerarPmocView(LoginRequiredMixin, PermissionRequiredMixin, View):
    context = {}
    raise_exception = True
    permission_required = (
        'cliente.add_registromanutencao',
    )

    def get(self, request, empresa, cliente):
        empresa = get_empresa(request, empresa)
        tecnico = empresa.tecnicos.get(pk=request.GET.get('tecnico'))
        cliente = empresa.clientes.get(pk=cliente)
        equipamento = cliente.equipamentos.get(pk=request.GET.get('equipamento'))

        dia, mes, ano = request.GET.get('start_date').split('/')

        meses = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[], 12:[]}

        
        try:
            for intervalo in empresa.manutencao_intervalo.all():
                qtd = int(12/int(360/intervalo.dias))
                
                o_list = []
                operacoes = intervalo.operacoes.filter(ativo=True)
                for o in operacoes:
                    o_list.append(o.pk)

                try:
                    for i in range(int(mes), 13, qtd):
                        meses[i] = meses[i] + list(o_list)
                except:
                    pass

            for m in meses:
                if meses[m]:
                    data_prevista = date(int(ano), m, 10)

                    registro_manutencao = RegistroManutencao(
                        cliente=cliente,
                        equipamento=equipamento,
                        tecnico=tecnico,
                        tipo=empresa.manutencao_tipo.get(nome='PREVENTIVA'),
                        data_prevista=data_prevista
                    )
                    registro_manutencao.save()

                    for i in meses[m]:
                        operacao = RegistroManutencaoOperacao(
                            registro_manutencao=registro_manutencao,
                            operacao=cliente.operacoes.get(pk=i)
                        )
                        operacao.save()
            
            messages.success(request, 'Plano de manutenção gerado com sucesso.')
        except:
            messages.error(request, 'Falha ao gerar plano de manutenção!')
        

        return HttpResponseRedirect(reverse_lazy(
            'empresa:cliente:ferramentas',
            kwargs={"empresa" : empresa.pk, "cliente" : cliente.pk}
        ))


# Ferramentas
ferramentas = FerramentasView.as_view()
ferramentas_gerar_pmoc = FerramentaGerarPmocView.as_view()