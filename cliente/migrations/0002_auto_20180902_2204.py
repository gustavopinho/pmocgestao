# Generated by Django 2.0.5 on 2018-09-03 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0001_initial'),
        ('cliente', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipamento',
            options={'ordering': ['ambiente__unidade', 'ambiente__atividade__nome', 'ambiente__nome', 'nome'], 'permissions': (('view_equipamento', 'Ver equipamento'),), 'verbose_name': 'Equipamento', 'verbose_name_plural': 'Equipamentos'},
        ),
        migrations.AlterModelOptions(
            name='operacao',
            options={'ordering': ['grupo__codigo', 'codigo', 'grupo__nome', 'nome'], 'permissions': (('view_operacao', 'Ver operações'),), 'verbose_name': 'Operação', 'verbose_name_plural': 'Operações'},
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='identificacao',
            field=models.CharField(blank=True, max_length=254, null=True, verbose_name='Identificação/Código'),
        ),
        migrations.RemoveField(
            model_name='registromanutencao',
            name='tecnico',
        ),
        migrations.AddField(
            model_name='registromanutencao',
            name='tecnico',
            field=models.ManyToManyField(related_name='manutencoes', to='empresa.Tecnico', verbose_name='Técnicos'),
        ),
    ]
