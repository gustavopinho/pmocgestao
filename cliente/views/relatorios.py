import functools
import operator
import calendar

from datetime import date, timedelta
from collections import OrderedDict
from dateutil.relativedelta import relativedelta

from django.shortcuts import render
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.views.generic import View

from core.utils import get_empresa, Month
from cliente.models import RegistroManutencao, RegistroManutencaoOperacao


class RelatoriosView(LoginRequiredMixin, PermissionRequiredMixin, View):
    template_name = 'cliente/relatorios.html'
    context = {}
    raise_exception = True
    permission_required = (
        'cliente.view_registromanutencao',
    )

    def get(self, request, empresa, cliente):
        self.context['empresa'] = get_empresa(request, empresa)
        self.context['cliente'] = self.context['empresa'].clientes.get(pk=cliente)
        self.context['equipamentos'] = self.context['cliente'].equipamentos.all()

        return render(request, self.template_name, self.context)


from core.render import PdfRender
class RelatorioPmocView(LoginRequiredMixin, PermissionRequiredMixin, View):
    template_name = 'cliente/relatorios/pmoc.html'
    context = {}
    raise_exception = True
    permission_required = (
        'cliente.view_registromanutencao',
    )

    def get(self, request, empresa, cliente):
        self.context['empresa'] = get_empresa(request, empresa)
        self.context['cliente'] = self.context['empresa'].clientes.get(pk=cliente)
        self.context['categorias'] = self.context['cliente'].operacao_grupo.all()
        self.context['equipamento'] = self.context['cliente'].equipamentos.get(pk=request.GET.get('equipamento'))

        self.context['date'] = request.GET.get('date')
        
        executado = request.GET.get('executado') or ''
        nexecutada = request.GET.get('nexecutada') or ''
        pmoca = request.GET.get('pmoca') or ''

        start_date = self.context['date'].split('/')
    
        start_date = date(int(start_date[2]), int(start_date[1]), int(start_date[0]))
        end_date = start_date + timedelta(days=365)

        self.context['start_date'] = start_date
        self.context['end_date'] = end_date

        today = date.today()

        m = date(start_date.year, start_date.month, 10)
        months = {}

        months[1] = {}
        months[1]['month'] = Month(m.year, m.month)

        for i in range(2, 13):
            m = m + relativedelta(months=1)
            months[i] = {}
            months[i]['month'] = Month(m.year, m.month)

        agenda = {}
        self.context['months'] = months
        for categoria in self.context['categorias']:
            for operacao in categoria.operacoes.all():
                
                # Agenda para salvar se as operações foram executadas
                agenda[operacao.pk] = {}

                # Intervalo em meses das manutenções
                qtd = int(12/int(360/operacao.intervalo.dias))
                # Mês de início do plano de manutenção para a operação
                m_start = 1

                if pmoca == 'PA':

                    # Verifica se a operação foi realizada anteriomente dentro do intervalo de manutenções
                    min_start_date = start_date - timedelta(days=operacao.intervalo.dias)
                    manutencao = RegistroManutencaoOperacao.objects.filter(
                        registro_manutencao__equipamento=self.context['equipamento'],
                        operacao=operacao,
                        registro_manutencao__data_prevista__range=(min_start_date, start_date),
                        registro_manutencao__tipo__nome='PREVENTIVA'
                    ).order_by('-registro_manutencao__data_prevista')[:1]

                    # Se existir alguma operação anterior então encontrar o prazo
                    if len(manutencao) > 0:
                        data_prevista = manutencao[0].registro_manutencao.data_prevista

                        #diff = months[1]['month'].month_date - data_prevista
                        proxima_manutencao = data_prevista + timedelta(days=operacao.intervalo.dias)
                        diff = proxima_manutencao - months[1]['month'].month_date

                        m_start += int(diff.days/30)


                # Preenche a agenda com todas as operações que já foram executadas
                for k, month in sorted(months.items()):
                    agenda[operacao.pk][k] = {}

                    if executado == 'E':
                        # Se executado E, se não verifica se ainda está no prazo, se sim A, se não NE
                        manutencoes_previstas = RegistroManutencaoOperacao.objects.filter(
                            registro_manutencao__equipamento=self.context['equipamento'],
                            operacao=operacao,
                            registro_manutencao__data_prevista__year=month['month'].month_date.year,
                            registro_manutencao__data_prevista__month=month['month'].month_date.month,
                            registro_manutencao__tipo__nome='PREVENTIVA'
                        ).order_by('-registro_manutencao__data_prevista')

                        if len(manutencoes_previstas) > 0:
                            agenda[operacao.pk][k]['exec'] = 'E'
                        else:
                            agenda[operacao.pk][k]['exec'] = '---'
                    else:
                        agenda[operacao.pk][k]['exec'] = '---'


                for i in range(m_start, 13, qtd):
                    if agenda[operacao.pk][i]['exec'] != 'E':
                        if nexecutada == 'NE':
                            # Verifica se a operação está em atraso
                            if today > months[i]['month'].month_date:
                                agenda[operacao.pk][i]['exec'] = 'NE'
                            else:
                                agenda[operacao.pk][i]['exec'] = 'A'
                        else:
                            agenda[operacao.pk][i]['exec'] = 'A'
        
        self.context['agenda'] = agenda
        self.context['manutencoes'] = RegistroManutencao.objects.filter(
            equipamento=self.context['equipamento'],
            data_prevista__range=(start_date, end_date),
            tipo__nome='PREVENTIVA',
            data_execucao__isnull=False
        )
        return PdfRender.render(self.template_name, self.context)

        return render(request, self.template_name, self.context)

# Relatórios
relatorios = RelatoriosView.as_view()
relatorio_pmoc = RelatorioPmocView.as_view()