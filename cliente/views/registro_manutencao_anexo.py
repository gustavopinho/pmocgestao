from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.http import JsonResponse
from django.views.generic import View

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from core.utils import get_empresa
from cliente.forms import RegistroManutencaoAnexoForm

class RegistroManutencaoAnexoListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    raise_exception = True
    permission_required = (
        'cliente.view_registromanutencaoanexo',
    )

    def get(self, request, empresa, cliente, manutencao):
        empresa = get_empresa(request, empresa)
        cliente = empresa.clientes.get(pk=cliente)
        manutencao = cliente.manutencoes.get(pk=manutencao)

        anexos = manutencao.anexos.all()
        results = [ob.to_json() for ob in anexos]
        return JsonResponse({'results': results})


class RegistroManutencaoAnexoCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    raise_exception = True
    permission_required = (
        'cliente.add_registromanutencaoanexo',
    )

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RegistroManutencaoAnexoCreateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, empresa, cliente, manutencao):
        empresa = get_empresa(request, empresa)
        cliente = empresa.clientes.get(pk=cliente)
        manutencao = cliente.manutencoes.get(pk=manutencao)

        form = RegistroManutencaoAnexoForm(request.POST, request.FILES)
        form.instance.registro_manutencao = manutencao

        if len(manutencao.anexos.all()) > 4:
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


class RegistroManutencaoAnexoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    raise_exception = True
    permission_required = (
        'cliente.delete_registromanutencaoanexo',
    )

    def get(self, request, empresa, cliente, manutencao, pk):
        empresa = get_empresa(request, empresa)
        cliente = empresa.clientes.get(pk=cliente)
        manutencao = cliente.manutencoes.get(pk=manutencao)
        anexo = manutencao.anexos.get(pk=pk)
        if anexo.delete():
            return JsonResponse({
                'success' : True,
                'message' : 'Anexo excluído com sucesso!'
            })

        return JsonResponse({
            'success' : True,
            'message' : 'Falha ao excluír anexo!'
        })


# Registro de Manutenção Anexos
registro_manutencao_anexo_list = RegistroManutencaoAnexoListView.as_view()
registro_manutencao_anexo_create = RegistroManutencaoAnexoCreateView.as_view()
registro_manutencao_anexo_delete = RegistroManutencaoAnexoDeleteView.as_view()