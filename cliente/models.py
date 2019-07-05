import os

from django.db import models
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.dispatch import receiver
from core.utils import ContentTypeRestrictedFileField
from pmoc.storage_backends import PrivateMediaStorage
from empresa.models import (
    Empresa, Responsavel, EquipamentoGrupo,
    Tecnico, ManutencaoTipo, UsuarioEmpresa,
    ManutencaoIntervalo
)


def client_equipamento_directory_path(instance, filename):
    return 'clientes/{0}/equipamentos/{1}/{2}'.format(
        instance.equipamento.cliente.pk,
        instance.equipamento.pk,
        filename
    )

def client_manutencao_directory_path(instance, filename):
    return 'clientes/{0}/equipamentos/{1}/manutencoes/{2}/{3}'.format(
        instance.registro_manutencao.cliente.pk,
        instance.registro_manutencao.equipamento.pk, 
        instance.registro_manutencao.pk,
        filename
    )

def client_anexo_directory_path(instance, filename):
    return 'clientes/{0}/anexos/{1}'.format(
        instance.cliente.pk,
        filename
    )


class Cliente(models.Model):
    """Clientes das empresas"""
    empresa = models.ForeignKey(Empresa, on_delete=models.DO_NOTHING, verbose_name='Empresa', related_name='clientes')
    nome = models.CharField('Nome', max_length=254)
    razao_social = models.CharField('Razão Social', max_length=254)
    cnpj = models.CharField('CNPJ', max_length=20, blank=True, null=True)
    
    logradouro = models.CharField('Logradouro', max_length=254, blank=True, null=True)
    numero = models.CharField('Número', max_length=20, blank=True, null=True)
    complemento = models.CharField('Complemento', max_length=254, blank=True, null=True)
    bairro = models.CharField('Bairro', max_length=254, blank=True, null=True)
    cidade = models.CharField('Cidade', max_length=254, blank=True, null=True)
    uf = models.CharField('UF', max_length=2, blank=True, null=True)
    cep = models.CharField('CEP', max_length=9, blank=True, null=True)
    
    email = models.CharField('Email', max_length=150, blank=True, null=True)
    fone = models.CharField('Telefone', max_length=15, blank=True, null=True)
    celular = models.CharField('Celular', max_length=15, blank=True, null=True)

    usuarios = models.ManyToManyField(UsuarioEmpresa, related_name='clientes', blank=True)

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']
        permissions = (
            ("view_cliente", "Ver cliente"),
        )

    def __str__(self):
        return self.nome

    def get_ano_manutencoes(self):
        start = self.manutencoes.all().order_by('data_prevista')[:1].get()
        end = self.manutencoes.all().order_by('-data_prevista')[:1].get()
        
        years = []
        for y in range(start.data_prevista.year, end.data_prevista.year+1):
            years.append(y)
        
        return years

    def get_qtd_unidades(self):
        return self.unidades.all().count()

    def get_qtd_ambientes(self):
        return self.ambientes.all().count()

    def get_qtd_equipamentos(self):
        return self.equipamentos.all().count()

    def get_qtd_equipamentos_ativos(self):
        return self.equipamentos.filter(ativo=True).count()

    def get_qtd_equipamentos_desativados(self):
        return self.equipamentos.filter(ativo=False).count()

    def get_qtd_manutencoes_agendadas(self):
        return self.manutencoes.filter(
            tipo__nome='PREVENTIVA',
            data_execucao__isnull=True
        ).count()

    def get_qtd_manutencoes_executadas(self):
        return self.manutencoes.filter(
            tipo__nome='PREVENTIVA',
            data_execucao__isnull=False
        ).count()


class Unidade(models.Model):
    """Endereço onde os clinte opera"""
    nome = models.CharField('Nome', max_length=254)

    cliente = models.ForeignKey('Cliente', on_delete=models.DO_NOTHING, verbose_name='Cliente', related_name='unidades')
    responsavel = models.ForeignKey(Responsavel, on_delete=models.DO_NOTHING, verbose_name='Responsável Técnico', related_name='unidades')
    
    logradouro = models.CharField('Logradouro', max_length=254, blank=True, null=True)
    numero = models.CharField('Número', max_length=20, blank=True, null=True)
    complemento = models.CharField('Complemento', max_length=254, blank=True, null=True)
    bairro = models.CharField('Bairro', max_length=254, blank=True, null=True)
    cidade = models.CharField('Cidade', max_length=254, blank=True, null=True)
    uf = models.CharField('UF', max_length=2, blank=True, null=True)
    cep = models.CharField('CEP', max_length=9, blank=True, null=True)

    email = models.CharField('Email', max_length=150, blank=True, null=True)
    fone = models.CharField('Telefone', max_length=15, blank=True, null=True)
    celular = models.CharField('Celular', max_length=15, blank=True, null=True)

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Unidade'
        verbose_name_plural = 'Unidades'
        ordering = ['nome']
        permissions = (
            ("view_unidade", "Ver unidade"),
        )

    def __str__(self):
        return self.nome


class Atividade(models.Model):
    """Atividade ao que o ambiente se destina"""
    cliente = models.ForeignKey('Cliente', on_delete=models.DO_NOTHING, verbose_name='Cliente', related_name='atividades')
    
    nome = models.CharField('Nome', max_length=254)

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Atividade'
        verbose_name_plural = 'Atividades'
        ordering = ['nome']
        permissions = (
            ("view_atividade", "Ver atividades"),
        )

    def __str__(self):
        return self.nome


class Ambiente(models.Model):
    """Relação de ambientes climatizados"""
    cliente = models.ForeignKey('Cliente', on_delete=models.DO_NOTHING, verbose_name='Cliente', related_name='ambientes')
    unidade = models.ForeignKey('Unidade', on_delete=models.DO_NOTHING, verbose_name='Unidade', related_name='ambientes')
    atividade = models.ForeignKey('Atividade', on_delete=models.DO_NOTHING, verbose_name='Departamento', related_name='ambientes')

    nome = models.CharField('Nome', max_length=254)

    identificacao = models.CharField('Identificação', max_length=50, blank=True, null=True)
    ocupantes = models.CharField('Ocupantes Fixo/Flutuantes', max_length=20, blank=True, null=True)
    area = models.IntegerField('Área em m²', blank=True, null=True)
    carga_termica = models.CharField('Carga Térmica BTU', max_length=50)

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Ambiente'
        verbose_name_plural = 'Ambientes'
        ordering = ['nome']
        permissions = (
            ("view_ambiente", "Ver Ambiente"),
        )

    def carga_termica_total(self):
        total = 0
        for equipamento in self.equipamentos.all():
            total = total + int(equipamento.capacidade_termica)
        return total

    def __str__(self):
        return self.unidade.nome + ' - ' + self.nome


class Equipamento(models.Model):
    """Relação de equipamentos de um ambiente"""
    cliente = models.ForeignKey('Cliente', on_delete=models.DO_NOTHING, verbose_name='Cliente', related_name='equipamentos')
    ambiente = models.ForeignKey('Ambiente', on_delete=models.DO_NOTHING, verbose_name='Ambiente', related_name='equipamentos')
    grupo = models.ForeignKey(EquipamentoGrupo, on_delete=models.DO_NOTHING, verbose_name='Grupo', related_name='equipamentos')
    
    nome = models.CharField('Nome', max_length=254)
    fabricante = models.CharField('Fabricante', max_length=254, blank=True, null=True)
    identificacao = models.CharField('Identificação/Código', max_length=254, blank=True, null=True)
    capacidade = models.CharField('Capacidade Térmica BTU', max_length=50)
    data_instalacao = models.DateField('Data de instalação:', null=True, blank=True)
    ativo = models.BooleanField('Ativo?', default=True)
    data_desativado = models.DateField('Data em que foi desativado?', null=True, blank=True)
    observacao = models.TextField('Observações', blank=True, null=True)

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Equipamento'
        verbose_name_plural = 'Equipamentos'
        ordering = ['ambiente__unidade','ambiente__atividade__nome', 'ambiente__nome', 'nome']
        permissions = (
            ("view_equipamento", "Ver equipamento"),
        )

    def __str__(self):
        return self.ambiente.unidade.nome + ' - ' + self.ambiente.nome + ' - ' + self.nome


class EquipamentoAnexo(models.Model):
    equipamento = models.ForeignKey('Equipamento', on_delete=models.DO_NOTHING, verbose_name='Equipamento', related_name='anexos')
    nome = models.CharField('Nome', max_length=254, blank=True, null=True)
    anexo = ContentTypeRestrictedFileField(
        'Anexo',
        upload_to=client_equipamento_directory_path,
        content_types=[
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/msword',
            'application/excel',
            'application/pdf',
            'application/txt',
            'image/gif',
            'image/jpeg',
            'image/png',
            'image/svg+xml',
            'application/x-rar-compressed',
            'application/octet-stream',
            'application/zip',
            'application/x-zip-compressed',
            'multipart/x-zip'
        ],
        max_upload_size=20971520,
        null=False, blank=False,
        default='',
        storage=PrivateMediaStorage()
    )
    
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Equipamento Anexo'
        verbose_name_plural = 'Equipamento Anexos'
        ordering = ['created']
        permissions = (
            ("view_equipamentoanexo", "Ver anexos do equipamento"),
        )

    def save(self, *args, **kwargs):
        if self.nome is None:
            self.nome = self.anexo.name
        super(EquipamentoAnexo, self).save(*args, **kwargs)


    def to_json(self):
        return dict(
            pk=self.pk,
            equipamento=self.equipamento.pk,
            anexo= self.anexo.url or '',
            nome= self.nome or self.anexo.name
        )

    def __str__(self):
        return self.nome or self.equipamento.nome


class OperacaoGrupo(models.Model):
    """Agrupamento das operações"""
    codigo = models.IntegerField('Código', blank=True, null=True)
    nome = models.CharField('Grupo descrição', max_length=254, blank=False, null=False)
    cliente = models.ForeignKey('Cliente', on_delete=models.DO_NOTHING, verbose_name='Cliente', related_name='operacao_grupo')
    equipamento_grupo = models.ForeignKey(EquipamentoGrupo, on_delete=models.DO_NOTHING, verbose_name='Grupo', related_name='operacao_grupo', default='')

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Grupo de Operação'
        verbose_name_plural = 'Grupos de Operação'
        ordering = ['codigo']
        permissions = (
            ("view_operacaogrupo", "Ver grupos de operação"),
        )

    def __str__(self):
        return "{0}. {1}".format(self.codigo, self.nome)

    def to_json(self):
        return dict(
            pk=self.pk,
            codigo=self.codigo,
            nome=self.nome
        )


class Operacao(models.Model):
    """Operações que serão feitas no registro de manutenção"""
    codigo = models.IntegerField('Código', blank=False, null=False)
    nome = models.CharField('Descrição', max_length=254, blank=False, null=False)
    cliente = models.ForeignKey('Cliente', on_delete=models.DO_NOTHING, verbose_name='Cliente', related_name='operacoes')
    grupo = models.ForeignKey('OperacaoGrupo', on_delete=models.DO_NOTHING, verbose_name='Grupo de Operação', related_name='operacoes')
    intervalo = models.ForeignKey(ManutencaoIntervalo, on_delete=models.DO_NOTHING, verbose_name='Intervalo entre manutenções', related_name='operacoes')
    ativo = models.BooleanField('Ativo?', default=True)

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Operação'
        verbose_name_plural = 'Operações'
        ordering = ['grupo__codigo', 'codigo', 'grupo__nome', 'nome']
        permissions = (
            ("view_operacao", "Ver operações"),
        )

    def __str__(self):
        return self.nome

    def to_json(self):
        return dict(
            pk=self.pk,
            codigo=self.codigo,
            nome=self.nome,
            intervalo=self.intervalo.nome
        )


class RegistroManutencao(models.Model):
    """Registra as manutenções executadas e manutenções agendadas"""
    cliente = models.ForeignKey('Cliente', on_delete=models.DO_NOTHING, verbose_name='Cliente', related_name='manutencoes')
    equipamento = models.ForeignKey('Equipamento', on_delete=models.DO_NOTHING, verbose_name='Equipamento', related_name='manutencoes')
    tecnico = models.ManyToManyField(Tecnico, verbose_name='Técnicos', related_name='manutencoes')
    tipo = models.ForeignKey(ManutencaoTipo, on_delete=models.DO_NOTHING, verbose_name='Tipo de Manutenção', related_name='manutencoes')

    data_prevista = models.DateField('Data Prevista', null=True, blank=True)
    data_execucao = models.DateField('Data da Execução', null=True, blank=True)

    observacao = models.TextField('Observações', null=True, blank=True)

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Registro de Manutenção'
        verbose_name_plural = 'Registro de Manutenções'
        ordering = ['data_prevista']
        permissions = (
            ("view_registromanutencao", "Ver Registro de Manutenção"),
        )

    def __str__(self):
        return self.equipamento.nome


class RegistroManutencaoAnexo(models.Model):
    registro_manutencao = models.ForeignKey('RegistroManutencao', on_delete=models.CASCADE, verbose_name='Registro de Manutencao', related_name='anexos')
    nome = models.CharField('Nome', max_length=254, blank=True, null=True)
    anexo = ContentTypeRestrictedFileField(
        'Anexo',
        upload_to=client_manutencao_directory_path,
        content_types=[
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/msword',
            'application/excel',
            'application/pdf',
            'application/txt',
            'image/gif',
            'image/jpeg',
            'image/png',
            'image/svg+xml',
            'application/x-rar-compressed',
            'application/octet-stream',
            'application/zip',
            'application/x-zip-compressed',
            'multipart/x-zip'
        ],
        max_upload_size=20971520,
        null=False, blank=False,
        default='',
        storage=PrivateMediaStorage()
    )
    
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Registro de Manutenção Anexo'
        verbose_name_plural = 'Registro de Manutenção Anexos'
        ordering = ['created']
        permissions = (
            ("view_registromanutencaoanexo", "Ver anexos do registro de manuteção"),
        )

    def save(self, *args, **kwargs):
        if self.nome is None:
            self.nome = self.anexo.name
        super(RegistroManutencaoAnexo, self).save(*args, **kwargs)


    def to_json(self):
        return dict(
            pk=self.pk,
            anexo= self.anexo.url or '',
            nome= self.nome or self.anexo.name
        )

    def __str__(self):
        return self.nome


class RegistroManutencaoOperacao(models.Model):
    """Usado para armazenar as operações do registros de manuteção"""
    registro_manutencao = models.ForeignKey('RegistroManutencao', on_delete=models.CASCADE, verbose_name='Registro de Manutencao', related_name='operacoes')
    operacao = models.ForeignKey(Operacao, on_delete=models.DO_NOTHING, verbose_name='Operação', related_name='manutencoes')

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Regitro de Manutenção Operação'
        verbose_name_plural = 'Registro de Manutenção Operações'
        ordering = ['operacao__grupo__codigo', 'operacao__codigo']
        permissions = (
            ("view_registromanutencaooperacao", "Ver Operações do Registro de Manutenção"),
        )

    def __str__(self):
        return self.operacao.nome

    def to_json(self):
        return dict(
            pk=self.pk,
            codigo="{0}.{1}".format(self.operacao.grupo.codigo, self.operacao.codigo),
            nome=self.operacao.nome,
            grupo=self.operacao.grupo.nome,
            intervalo=self.operacao.intervalo.nome
        )


class Medicoes(models.Model):
    """Adiciona medições feitas durante uma operação"""
    registro_manutencao = models.ForeignKey('RegistroManutencao', on_delete=models.CASCADE, verbose_name='Registro de Manutencao', related_name='medicoes')

    pressao_baixa = models.CharField('Pressão Baixa', max_length=10, null=True, blank=True)
    pressao_alta = models.CharField('Pressão Alta', max_length=10, null=True, blank=True)
    temperatura_insuflamento = models.CharField('Temperatura de Insuflamento', max_length=10, null=True, blank=True)
    temperatura_retorno = models.CharField('Temperatura de Retorno', max_length=10, null=True, blank=True)
    tensao = models.CharField('Tensão', max_length=10, null=True, blank=True)
    corrente = models.CharField('Corrente', max_length=10, null=True, blank=True)
    observacao = models.TextField('Observações', null=True, blank=True)

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Medição'
        verbose_name_plural = 'Medições'
        ordering = ['created']
        permissions = (
            ("view_medicoes", "Ver Medições"),
        )

    def __str__(self):
        return self.created

    def to_json(self):
        return dict(
            pk=self.pk,
            pressao_baixa=self.pressao_baixa,
            pressao_alta=self.pressao_alta,
            temperatura_insuflamento=self.temperatura_insuflamento,
            temperatura_retorno=self.temperatura_retorno,
            tensao=self.tensao,
            corrente=self.corrente,
            observacao=self.observacao
        )


class Anexo(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.DO_NOTHING, verbose_name='Cliente', related_name='anexos')
    nome = models.CharField('Nome', max_length=254, blank=True, null=True)
    anexo = ContentTypeRestrictedFileField(
        'Anexo',
        upload_to=client_anexo_directory_path,
        content_types=[
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/msword',
            'application/excel',
            'application/pdf',
            'application/txt',
            'image/gif',
            'image/jpeg',
            'image/png',
            'image/svg+xml',
            'application/x-rar-compressed',
            'application/octet-stream',
            'application/zip',
            'application/x-zip-compressed',
            'multipart/x-zip'

        ],
        max_upload_size=20971520,
        null=False, blank=False,
        default='',
        storage=PrivateMediaStorage()
    )
    
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Anexo'
        verbose_name_plural = 'Anexos'
        ordering = ['-created']
        permissions = (
            ("view_anexo", "Ver anexos"),
        )

    def save(self, *args, **kwargs):
        if self.nome is None:
            self.nome = self.anexo.name
        super(Anexo, self).save(*args, **kwargs)


    def to_json(self):
        return dict(
            pk=self.pk,
            anexo= self.anexo.url or '',
            nome= self.nome or self.anexo.name
        )

    def __str__(self):
        return self.nome
        


@receiver(models.signals.post_delete, sender=EquipamentoAnexo)
@receiver(models.signals.post_delete, sender=RegistroManutencaoAnexo)
@receiver(models.signals.post_delete, sender=Anexo)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    
    if instance.anexo:
        instance.anexo.delete(save=False)


@receiver(models.signals.pre_save, sender=EquipamentoAnexo)
@receiver(models.signals.pre_save, sender=RegistroManutencaoAnexo)
@receiver(models.signals.post_delete, sender=Anexo)
def auto_delete_file_on_change(sender, instance, **kwargs):
    
    if not instance.pk:
        return False

    try:
        old_file = EquipamentoAnexo.objects.get(pk=instance.pk).anexo
    except EquipamentoAnexo.DoesNotExist:
        return False

    new_file = instance.anexo
    if not old_file == new_file or new_file is None:
        old_file.delete(save=False)