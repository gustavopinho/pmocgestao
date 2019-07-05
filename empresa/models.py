import os
from uuid import uuid4

from django.db import models
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.dispatch import receiver
from django.contrib.auth.models import Group

from accounts.models import User


def path_and_rename(instance, filename):
    return os.path.join('empresas', "{0}.{1}".format(slugify(instance.nome), filename.split('.')[-1]))

class Empresa(models.Model):
    """Registro das empresas que usam o sistema"""
    nome = models.CharField('Nome Fantasia', max_length=254)
    razao_social = models.CharField('Razão social', max_length=254)
    cnpj = models.CharField('CNPJ', max_length=50)

    logradouro = models.CharField('Logradouro', max_length=254, blank=True, null=True)
    numero = models.CharField('Número', max_length=20, blank=True, null=True)
    complemento = models.CharField('Complemento', max_length=254, blank=True, null=True)
    bairro = models.CharField('Bairro', max_length=254, blank=True, null=True)
    cidade = models.CharField('Cidade', max_length=254, blank=True, null=True)
    uf = models.CharField('UF', max_length=2, blank=True, null=True)
    cep = models.CharField('CEP', max_length=9, blank=True, null=True)
    
    email = models.EmailField('Email', max_length=150, blank=True, null=True)
    fone = models.CharField('Telefone', max_length=15, blank=True, null=True)
    celular = models.CharField('Celular', max_length=15, blank=True, null=True)

    logo = models.FileField(
        'Logo', upload_to=path_and_rename, blank=True, null=True
    )

    # Cofigurações para controle
    max_equipamentos = models.IntegerField('Código', blank=True, null=True, default=50)
    ativo = models.BooleanField('Ativo?', default=True)

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['nome']
        permissions = (
            ("view_empresa", "Ver empresa"),
        )

    def __str__(self):
        return self.nome

    def get_ano_manutencoes(self):
        years = []
        for cliente in self.clientes.all():
            for year in cliente.get_ano_manutencoes():
                if not year in years:
                    years.append(year)
        return years


    def get_qtd_equipamentos(self):
        total = 0
        for cliente in self.clientes.all():
            total = total + cliente.get_qtd_equipamentos()
        return total

    def get_qtd_equipamentos_ativos(self):
        total = 0
        for cliente in self.clientes.all():
            total = total + cliente.get_qtd_equipamentos_ativos()
        return total

    def get_qtd_equipamentos_desativados(self):
        total = 0
        for cliente in self.clientes.all():
            total = total + cliente.get_qtd_equipamentos_desativados()
        return total


class UsuarioEmpresa(models.Model):
    """Empresas que o usuário tem acesso"""
    ACESSO_CHOICES = (
        ('REMOVER', 'Acesso Removido'),
        ('PMOCADMIN', 'Acesso Administrador'),
        ('PMOCCLIENTE', 'Acesso Cliente'),
        ('PMOCTECNICO', 'Acesso Técnico'),
    )
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Tipo de Empresa', related_name='empresas')
    empresa = models.ForeignKey('Empresa', on_delete=models.DO_NOTHING, verbose_name='Empresas', related_name='usuarios')

    acesso = models.CharField(
        'Acesso ao sistema',
        max_length=20,
        choices=ACESSO_CHOICES,
        blank=True, null=True
    )

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        unique_together = (('usuario', 'empresa'),)
        verbose_name = 'Usuário Empresa'
        verbose_name_plural = 'Usuários Empresa'
        ordering = ['id']

    def save(self, *args, **kwargs):
        if self.acesso == 'REMOVER':
            self.usuario.groups.clear()

        if self.acesso in ['PMOCADMIN', 'PMOCCLIENTE', 'PMOCTECNICO']:
            grupo = Group.objects.get(name=self.acesso)
            self.usuario.groups.add(grupo)
        
        super(UsuarioEmpresa, self).save(*args, **kwargs)

    def __str__(self):
        return self.usuario.name or self.usuario.username


class Responsavel(models.Model):
    """Responsáveis técnicos da empresa que serão usados no relatório PMOC"""
    empresa = models.ForeignKey('Empresa', on_delete=models.DO_NOTHING, verbose_name='Empresa', related_name='responsaveis')
    nome = models.CharField('Nome', max_length=254)
    cnpj = models.CharField('CNPJ/CPF', max_length=20)

    logradouro = models.CharField('Logradouro', max_length=254, blank=True, null=True)
    numero = models.CharField('Número', max_length=20, blank=True, null=True)
    complemento = models.CharField('Complemento', max_length=254, blank=True, null=True)
    bairro = models.CharField('Bairro', max_length=254, blank=True, null=True)
    cidade = models.CharField('Cidade', max_length=254, blank=True, null=True)
    uf = models.CharField('UF', max_length=2, blank=True, null=True)
    cep = models.CharField('CEP', max_length=9, blank=True, null=True)

    email = models.CharField('Email', max_length=150, blank=True, null=True)
    fone = models.CharField('Telefone', max_length=15, blank=True, null=True)
    registro_conselho = models.CharField('Registro no Conselho', max_length=50)

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Responsável Técnico'
        verbose_name_plural = 'Responsáveis Técnico'
        ordering = ['nome']
        permissions = (
            ("view_responsavel", "Ver técnico"),
        )

    def __str__(self):
        return self.nome


class Tecnico(models.Model):
    """Técnicos responsáveis pelas operações"""
    empresa = models.ForeignKey('Empresa', on_delete=models.DO_NOTHING, verbose_name='Empresas', related_name='tecnicos')
    nome = models.CharField('Nome', max_length=254)

    logradouro = models.CharField('Logradouro', max_length=254, blank=True, null=True)
    numero = models.CharField('Número', max_length=20, blank=True, null=True)
    complemento = models.CharField('Complemento', max_length=254, blank=True, null=True)
    bairro = models.CharField('Bairro', max_length=254, blank=True, null=True)
    cidade = models.CharField('Cidade', max_length=254, blank=True, null=True)
    uf = models.CharField('UF', max_length=2, blank=True, null=True)
    cep = models.CharField('Cep', max_length=9, blank=True, null=True)

    email = models.CharField('Email', max_length=150, blank=True, null=True)
    fone = models.CharField('Telefone', max_length=15, blank=True, null=True)

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Técnico'
        verbose_name_plural = 'Técnicos'
        ordering = ['nome']
        permissions = (
            ("view_tecnico", "Ver técnico"),
        )

    def __str__(self):
        return self.nome


class EquipamentoGrupo(models.Model):
    """Categorias dos equipamentos"""
    nome = models.CharField('Nome', max_length=254, blank=False, null=False)
    empresa = models.ForeignKey('Empresa', on_delete=models.DO_NOTHING, verbose_name='Empresas', related_name='equipamento_grupos')

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Equipamento Grupo'
        verbose_name_plural = 'Equipamento Grupos'
        ordering = ['nome']
        permissions = (
            ("view_equipamentogrupo", "Ver empresa"),
        )

    def __str__(self):
        return self.nome


class ManutencaoTipo(models.Model):
    """Tipo de Manutenção ex. Preventiva e Corretiva"""
    nome = models.CharField('Nome', max_length=254, blank=False, null=False)
    empresa = models.ForeignKey('Empresa', on_delete=models.DO_NOTHING, verbose_name='Empresas', related_name='manutencao_tipo')

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Tipo de Manutenção'
        verbose_name_plural = 'Tipos de Manutenção'
        ordering = ['nome']
        permissions = (
            ("view_manutencaotipo", "Ver tipo de manutenção"),
        )

    def __str__(self):
        return self.nome


class ManutencaoIntervalo(models.Model):
    """Intervalo entre as manuteções, por operação"""
    nome = models.CharField('Descrição', max_length=254)
    dias = models.IntegerField('Intervalo (em dias)', blank=False, null=False)
    empresa = models.ForeignKey('Empresa', on_delete=models.DO_NOTHING, verbose_name='Empresas', related_name='manutencao_intervalo')

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Intervalo de Manutenção'
        verbose_name_plural = 'Intervalos de Manutenção'
        ordering = ['nome']
        permissions = (
            ("view_manutencaointervalo", "Ver intervalos de manutenção"),
        )

    def __str__(self):
        return self.nome


@receiver(models.signals.post_delete, sender=Empresa)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.logo:
        instance.logo.delete(save=False)


@receiver(models.signals.pre_save, sender=Empresa)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Empresa.objects.get(pk=instance.pk).logo
    except Empresa.DoesNotExist:
        return False

    new_file = instance.logo
    if not old_file == new_file or new_file is None:
        old_file.delete(save=False)