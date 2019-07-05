from django.forms import ModelForm

from .models import Empresa, UsuarioEmpresa

class EmpresaForm(ModelForm):

    class Meta:
        model = Empresa
        fields = '__all__'
        exclude = ['id', 'created', 'modified']


class UsuarioEmpresaForm(ModelForm):

    class Meta:
        model = UsuarioEmpresa
        fields = '__all__'
        exclude = ['id', 'usuario', 'empresa', 'created', 'modified']
        