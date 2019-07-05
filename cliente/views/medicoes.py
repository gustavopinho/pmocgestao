from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.http import JsonResponse
from django.views.generic import View

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from cliente.forms import MedicoesForm
from core.utils import get_empresa


class AllMedicoesView(LoginRequiredMixin, PermissionRequiredMixin, View):
    raise_exception = True
    permission_required = (
        'cliente.view_medicoes',
    )
    def get(self, request, empresa, cliente, manutencao):
        empresa = get_empresa(request, empresa)
        cliente = empresa.clientes.get(pk=cliente)
        manutencao = cliente.manutencoes.get(pk=manutencao)
        medicoes = manutencao.medicoes.all()
        results = [ob.to_json() for ob in medicoes]
        return JsonResponse({'results': results})


class SaveMedicoesView(LoginRequiredMixin, PermissionRequiredMixin, View):
    form = MedicoesForm
    raise_exception = True
    permission_required = (
        'cliente.add_medicoes',
        'cliente.change_medicoes',
    )

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SaveMedicoesView, self).dispatch(request, *args, **kwargs)

    def get(self, request, empresa, cliente, manutencao, pk=None):
        empresa = get_empresa(request, empresa)
        cliente = empresa.clientes.get(pk=cliente)
        manutencao = cliente.manutencoes.get(pk=manutencao)
        medicoes = manutencao.medicoes.get(pk=pk)
        return JsonResponse({'result': medicoes.to_json()})

    def post(self, request, empresa, cliente, manutencao, pk=None):
        empresa = get_empresa(request, empresa)
        cliente = empresa.clientes.get(pk=cliente)
        manutencao = cliente.manutencoes.get(pk=manutencao)
        if pk is not None:
            medicoes = manutencao.medicoes.get(pk=pk)
            form = self.form(request.POST, instance=medicoes)
        else:
            form = self.form(request.POST)

        form.instance.registro_manutencao = manutencao

        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Registro salvo com sucesso!'})
        else:
            return JsonResponse({'message': 'Ocorreu um erro ao salvar!'})


class DeleteMedicoesView(LoginRequiredMixin, PermissionRequiredMixin, View):
    raise_exception = True
    permission_required = (
        'cliente.delete_medicoes',
    )

    def get(self, request, empresa, cliente, manutencao, pk):
        try:
            empresa = get_empresa(request, empresa)
            cliente = empresa.clientes.get(pk=cliente)
            manutencao = cliente.manutencoes.get(pk=manutencao)
            medicoes = manutencao.medicoes.get(pk=pk)

            medicoes.delete()
            return JsonResponse({'message': 'Medição excluída com sucesso!'})
        except:
            return JsonResponse({'message': 'Falha ao excluír medição!'})

# Medições
all_medicoes = AllMedicoesView.as_view()
save_medicoes = SaveMedicoesView.as_view()
delete_medicoes = DeleteMedicoesView.as_view()
