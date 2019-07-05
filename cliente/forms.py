from django import forms

from .models import Medicoes, EquipamentoAnexo, RegistroManutencaoAnexo

class MedicoesForm(forms.ModelForm):

    class Meta:
        model = Medicoes
        fields = '__all__'
        exclude = ['id', 'registro_manutencao', 'created', 'modified']


class RegistroManutencaoFilter(forms.Form):
    OPCAO = (
        ('', '---'),
        ('1', 'Sim'),
        ('2', 'Não')
    )
    unidade = forms.ModelMultipleChoiceField(label='Unidade', queryset=None, required=False)
    tipo = forms.ModelMultipleChoiceField(label='Tipo de Manutenção', queryset=None, required=False)
    equipamentos = forms.ModelMultipleChoiceField(label='Equipamentos', queryset=None, required=False)
    executado = forms.ChoiceField(label='Executado?', choices=OPCAO, required=False)
    date_start = forms.DateField(label='Data inicial prevista', required=False)
    date_end = forms.DateField(label='Data limite prevista', required=False)

    def __init__(self, cliente, *args, **kwargs):
        super(RegistroManutencaoFilter, self).__init__(*args, **kwargs)
        
        self.fields['unidade'].queryset = cliente.unidades.all()
        self.fields['tipo'].queryset = cliente.empresa.manutencao_tipo.all()
        self.fields['equipamentos'].queryset = cliente.equipamentos.all()


class EquipamentoAnexoForm(forms.ModelForm):

    class Meta:
        model = EquipamentoAnexo
        fields = '__all__'
        exclude = ['id', 'equipamento', 'created', 'modified']


class RegistroManutencaoAnexoForm(forms.ModelForm):

    class Meta:
        model = RegistroManutencaoAnexo
        fields = '__all__'
        exclude = ['id', 'registro_manutencao', 'created', 'modified']
        
