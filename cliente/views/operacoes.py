from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.http import JsonResponse
from django.views.generic import View

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from cliente.models import RegistroManutencaoOperacao
from core.utils import get_empresa

class GrupoOperacaoView(LoginRequiredMixin, PermissionRequiredMixin, View):
    raise_exception = True
    permission_required = (
        'cliente.view_operacaogrupo',
    )

    def get(self, request, empresa, cliente, manutencao):
        empresa = get_empresa(request, empresa)
        cliente = empresa.clientes.get(pk=cliente)
        manutencao = cliente.manutencoes.get(pk=manutencao)

        grupo_operacao = manutencao.equipamento.grupo.operacao_grupo.filter(cliente=cliente)
        results = [ob.to_json() for ob in grupo_operacao]
        return JsonResponse({'results': results})


class OperacoesView(LoginRequiredMixin, PermissionRequiredMixin, View):
    raise_exception = True
    permission_required = (
        'cliente.view_operacao',
    )

    def get(self, request, empresa, cliente, manutencao, pk):
        empresa = get_empresa(request, empresa)
        cliente = empresa.clientes.get(pk=cliente)
        manutencao = cliente.manutencoes.get(pk=manutencao)

        grupo = cliente.operacao_grupo.get(pk=pk)

        exclude = []
        for o in manutencao.operacoes.all():
            exclude.append(o.operacao.pk)
        
        operacoes = grupo.operacoes.filter(ativo=True).exclude(pk__in=exclude)
        results = [ob.to_json() for ob in operacoes]
        return JsonResponse({'results': results})


class AllManutencaoOperacaoView(LoginRequiredMixin, PermissionRequiredMixin, View):
    raise_exception = True
    permission_required = (
        'cliente.view_registromanutencaooperacao',
    )

    def get(self, request, empresa, cliente, manutencao):
        empresa = get_empresa(request, empresa)
        cliente = empresa.clientes.get(pk=cliente)
        manutencao = cliente.manutencoes.get(pk=manutencao)
        operacoes = manutencao.operacoes.all()

        results = [ob.to_json() for ob in operacoes]
        return JsonResponse({'results': results})


class SaveManutencaoOperacaoView(LoginRequiredMixin, PermissionRequiredMixin, View):
    raise_exception = True
    permission_required = (
        'cliente.add_registromanutencaooperacao',
    )

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SaveManutencaoOperacaoView, self).dispatch(request, *args, **kwargs)

    def post(self, request, empresa, cliente, manutencao):
        empresa = get_empresa(request, empresa)
        cliente = empresa.clientes.get(pk=cliente)
        manutencao = cliente.manutencoes.get(pk=manutencao)

        operacoes = request.POST.get('operacoes').split(',')
        for operacao in operacoes:
            try:
                manutencao.operacoes.get(operacao__pk=operacao)
            except RegistroManutencaoOperacao.DoesNotExist:
                registro_manutencao_operacao = RegistroManutencaoOperacao(
                    registro_manutencao=manutencao,
                    operacao=cliente.operacoes.get(pk=int(operacao))
                )
                registro_manutencao_operacao.save()

        return JsonResponse({'message': 'Operações adicionadas com sucesso!'})


class DeleteManutencaoOperacaoView(LoginRequiredMixin, PermissionRequiredMixin, View):
    raise_exception = True
    permission_required = (
        'cliente.delete_registromanutencaooperacao',
    )

    def get(self, request, empresa, cliente, manutencao, pk):
        try:
            empresa = get_empresa(request, empresa)
            cliente = empresa.clientes.get(pk=cliente)
            manutencao = cliente.manutencoes.get(pk=manutencao)
            operacao = manutencao.operacoes.get(pk=pk)
            operacao.delete()
            return JsonResponse({'message': 'Operação excluída com sucesso!'})
        except:
            return JsonResponse({'message': 'Falha ao excluír operação!'})


# Operações
grupo_operacao = GrupoOperacaoView.as_view()
operacoes = OperacoesView.as_view()
all_manutencao_operacao = AllManutencaoOperacaoView.as_view()
save_manutencao_operacao = SaveManutencaoOperacaoView.as_view()
delete_manutencao_operacao = DeleteManutencaoOperacaoView.as_view()