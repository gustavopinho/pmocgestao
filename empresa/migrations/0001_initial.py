# Generated by Django 2.0.5 on 2018-06-02 14:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import empresa.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=254, verbose_name='Nome Fantasia')),
                ('razao_social', models.CharField(max_length=254, verbose_name='Razão social')),
                ('cnpj', models.CharField(max_length=50, verbose_name='CNPJ')),
                ('logradouro', models.CharField(blank=True, max_length=254, null=True, verbose_name='Logradouro')),
                ('numero', models.CharField(blank=True, max_length=20, null=True, verbose_name='Número')),
                ('complemento', models.CharField(blank=True, max_length=254, null=True, verbose_name='Complemento')),
                ('bairro', models.CharField(blank=True, max_length=254, null=True, verbose_name='Bairro')),
                ('cidade', models.CharField(blank=True, max_length=254, null=True, verbose_name='Cidade')),
                ('uf', models.CharField(blank=True, max_length=2, null=True, verbose_name='UF')),
                ('cep', models.CharField(blank=True, max_length=9, null=True, verbose_name='CEP')),
                ('email', models.EmailField(blank=True, max_length=150, null=True, verbose_name='Email')),
                ('fone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefone')),
                ('celular', models.CharField(blank=True, max_length=15, null=True, verbose_name='Celular')),
                ('logo', models.FileField(blank=True, null=True, upload_to=empresa.models.path_and_rename, verbose_name='Logo')),
                ('max_equipamentos', models.IntegerField(blank=True, default=50, null=True, verbose_name='Código')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
            ],
            options={
                'verbose_name': 'Empresa',
                'permissions': (('view_empresa', 'Ver empresa'),),
                'ordering': ['nome'],
                'verbose_name_plural': 'Empresas',
            },
        ),
        migrations.CreateModel(
            name='EquipamentoGrupo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=254, verbose_name='Nome')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='equipamento_grupos', to='empresa.Empresa', verbose_name='Empresas')),
            ],
            options={
                'verbose_name': 'Equipamento Grupo',
                'permissions': (('view_equipamentogrupo', 'Ver empresa'),),
                'ordering': ['nome'],
                'verbose_name_plural': 'Equipamento Grupos',
            },
        ),
        migrations.CreateModel(
            name='ManutencaoIntervalo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=254, verbose_name='Descrição')),
                ('dias', models.IntegerField(verbose_name='Intervalo (em dias)')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='manutencao_intervalo', to='empresa.Empresa', verbose_name='Empresas')),
            ],
            options={
                'verbose_name': 'Intervalo de Manutenção',
                'permissions': (('view_manutencaointervalo', 'Ver intervalos de manutenção'),),
                'ordering': ['nome'],
                'verbose_name_plural': 'Intervalos de Manutenção',
            },
        ),
        migrations.CreateModel(
            name='ManutencaoTipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=254, verbose_name='Nome')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='manutencao_tipo', to='empresa.Empresa', verbose_name='Empresas')),
            ],
            options={
                'verbose_name': 'Tipo de Manutenção',
                'permissions': (('view_manutencaotipo', 'Ver tipo de manutenção'),),
                'ordering': ['nome'],
                'verbose_name_plural': 'Tipos de Manutenção',
            },
        ),
        migrations.CreateModel(
            name='Responsavel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=254, verbose_name='Nome')),
                ('cnpj', models.CharField(max_length=20, verbose_name='CNPJ/CPF')),
                ('logradouro', models.CharField(blank=True, max_length=254, null=True, verbose_name='Logradouro')),
                ('numero', models.CharField(blank=True, max_length=20, null=True, verbose_name='Número')),
                ('complemento', models.CharField(blank=True, max_length=254, null=True, verbose_name='Complemento')),
                ('bairro', models.CharField(blank=True, max_length=254, null=True, verbose_name='Bairro')),
                ('cidade', models.CharField(blank=True, max_length=254, null=True, verbose_name='Cidade')),
                ('uf', models.CharField(blank=True, max_length=2, null=True, verbose_name='UF')),
                ('cep', models.CharField(blank=True, max_length=9, null=True, verbose_name='CEP')),
                ('email', models.CharField(blank=True, max_length=150, null=True, verbose_name='Email')),
                ('fone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefone')),
                ('registro_conselho', models.CharField(max_length=50, verbose_name='Registro no Conselho')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='responsaveis', to='empresa.Empresa', verbose_name='Empresa')),
            ],
            options={
                'verbose_name': 'Responsável Técnico',
                'permissions': (('view_responsavel', 'Ver técnico'),),
                'ordering': ['nome'],
                'verbose_name_plural': 'Responsáveis Técnico',
            },
        ),
        migrations.CreateModel(
            name='Tecnico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=254, verbose_name='Nome')),
                ('logradouro', models.CharField(blank=True, max_length=254, null=True, verbose_name='Logradouro')),
                ('numero', models.CharField(blank=True, max_length=20, null=True, verbose_name='Número')),
                ('complemento', models.CharField(blank=True, max_length=254, null=True, verbose_name='Complemento')),
                ('bairro', models.CharField(blank=True, max_length=254, null=True, verbose_name='Bairro')),
                ('cidade', models.CharField(blank=True, max_length=254, null=True, verbose_name='Cidade')),
                ('uf', models.CharField(blank=True, max_length=2, null=True, verbose_name='UF')),
                ('cep', models.CharField(blank=True, max_length=9, null=True, verbose_name='Cep')),
                ('email', models.CharField(blank=True, max_length=150, null=True, verbose_name='Email')),
                ('fone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefone')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tecnicos', to='empresa.Empresa', verbose_name='Empresas')),
            ],
            options={
                'verbose_name': 'Técnico',
                'permissions': (('view_tecnico', 'Ver técnico'),),
                'ordering': ['nome'],
                'verbose_name_plural': 'Técnicos',
            },
        ),
        migrations.CreateModel(
            name='UsuarioEmpresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acesso', models.CharField(blank=True, choices=[('REMOVER', 'Acesso Removido'), ('PMOCADMIN', 'Acesso Administrador'), ('PMOCCLIENTE', 'Acesso Cliente'), ('PMOCTECNICO', 'Acesso Técnico')], max_length=20, null=True, verbose_name='Acesso ao sistema')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='usuarios', to='empresa.Empresa', verbose_name='Empresas')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empresas', to=settings.AUTH_USER_MODEL, verbose_name='Tipo de Empresa')),
            ],
            options={
                'verbose_name': 'Usuário Empresa',
                'ordering': ['id'],
                'verbose_name_plural': 'Usuários Empresa',
            },
        ),
        migrations.AlterUniqueTogether(
            name='usuarioempresa',
            unique_together={('usuario', 'empresa')},
        ),
    ]
