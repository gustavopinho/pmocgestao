from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.http import JsonResponse
from django.views.generic import View

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from cliente.forms import EquipamentoAnexoForm
from core.utils import get_empresa


class EquipamentoAnexoListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    raise_exception = True
    permission_required = (
        'cliente.view_equipamentoanexo',
    )

    def get(self, request, empresa, cliente, equipamento):
        empresa = get_empresa(request, empresa)
        cliente = empresa.clientes.get(pk=cliente)
        equipamento = cliente.equipamentos.get(pk=equipamento)

        anexos = equipamento.anexos.all()
        results = [ob.to_json() for ob in anexos]
        return JsonResponse({'results': results})


class EquipamentoAnexoCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    raise_exception = True
    permission_required = (
        'cliente.add_equipamentoanexo',
    )

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(EquipamentoAnexoCreateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, empresa, cliente, equipamento):
        empresa = get_empresa(request, empresa)
        cliente = empresa.clientes.get(pk=cliente)
        equipamento = cliente.equipamentos.get(pk=equipamento)

        form = EquipamentoAnexoForm(request.POST, request.FILES)
        form.instance.equipamento = equipamento

        if len(equipamento.anexos.all()) > 4:
            return JsonResponse({
                'success' : False,
                'message' : 'Quantidade máxima de anexos excedida!'
            })
        
        if form.is_valid:
            form.save()
            return JsonResponse({
                'success' : True,
                'message' : 'Anexo inserido com sucesso!'
            })

        return JsonResponse({
            'success' : True,
            'messages' : form.errors.items()
        })


class EquipamentoAnexoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    raise_exception = True
    permission_required = (
        'cliente.delete_equipamentoanexo',
    )

    def get(self, request, empresa, cliente, equipamento, pk):
        empresa = get_empresa(request, empresa)
        cliente = empresa.clientes.get(pk=cliente)
        equipamento = cliente.equipamentos.get(pk=equipamento)
        anexo = equipamento.anexos.get(pk=pk)
        if anexo.delete():
            return JsonResponse({
                'success' : True,
                'message' : 'Anexo excluído com sucesso!'
            })

        return JsonResponse({
            'success' : True,
            'message' : 'Falha ao excluír anexo!'
        })


# Equipamento Anexos
equipamento_anexo_list = EquipamentoAnexoListView.as_view()
equipamento_anexo_create = EquipamentoAnexoCreateView.as_view()
equipamento_anexo_delete = EquipamentoAnexoDeleteView.as_view()