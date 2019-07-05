from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from .views import (
    cliente, unidade, atividade,
    ambiente, equipamento, operacao_grupo,
    operacao, registro_manutencao, medicoes,
    operacoes, equipamento_anexo, registro_manutencao_anexo,
    anexo, relatorios

)

app_name = 'cliente'
urlpatterns = [
    # Cliente
    path('<int:pk>/dashboard', cliente.cliente_dashboard, name='cliente_dashboard'),
    path('<int:pk>/dashboard/relatorios', cliente.cliente_relatorios, name='cliente_relatorios'),
    path('create', cliente.cliente_create, name='cliente_create'),
    path('create/<int:pk>', cliente.cliente_update, name='cliente_update'),
    # Unidade
    path('<int:cliente>/unidade', unidade.unidade_list, name='unidade_list'),
    path('<int:cliente>/unidade/create', unidade.unidade_create, name='unidade_create'),
    path('<int:cliente>/unidade/detail/<int:pk>/', unidade.unidade_detail, name='unidade_detail'),
    path('<int:cliente>/unidade/update/<int:pk>/', unidade.unidade_update, name='unidade_update'),
    path('<int:cliente>/unidade/delete/<int:pk>/', unidade.unidade_delete, name='unidade_delete'),
    # Atividade
    path('<int:cliente>/atividade', atividade.atividade_list, name='atividade_list'),
    path('<int:cliente>/atividade/create', atividade.atividade_create, name='atividade_create'),
    path('<int:cliente>/atividade/update/<int:pk>/', atividade.atividade_update, name='atividade_update'),
    path('<int:cliente>/atividade/delete/<int:pk>/', atividade.atividade_delete, name='atividade_delete'),
    # Ambiente
    path('<int:cliente>/ambiente', ambiente.ambiente_list, name='ambiente_list'),
    path('<int:cliente>/ambiente/create', ambiente.ambiente_create, name='ambiente_create'),
    path('<int:cliente>/ambiente/update/<int:pk>/', ambiente.ambiente_update, name='ambiente_update'),
    path('<int:cliente>/ambiente/delete/<int:pk>/', ambiente.ambiente_delete, name='ambiente_delete'),
    # Equipamento
    path('<int:cliente>/equipamento', equipamento.equipamento_list, name='equipamento_list'),
    path('<int:cliente>/equipamento/create', equipamento.equipamento_create, name='equipamento_create'),
    path('<int:cliente>/equipamento/detail/<int:pk>/', equipamento.equipamento_detail, name='equipamento_detail'),
    path('<int:cliente>/equipamento/update/<int:pk>/', equipamento.equipamento_update, name='equipamento_update'),
    path('<int:cliente>/equipamento/delete/<int:pk>/', equipamento.equipamento_delete, name='equipamento_delete'),
    # Grupo de operações
    path('<int:cliente>/operacao-grupo', operacao_grupo.operacao_grupo_list, name='operacao_grupo_list'),
    path('<int:cliente>/operacao-grupo/create', operacao_grupo.operacao_grupo_create, name='operacao_grupo_create'),
    path('<int:cliente>/operacao-grupo/update/<int:pk>/', operacao_grupo.operacao_grupo_update, name='operacao_grupo_update'),
    path('<int:cliente>/operacao-grupo/delete/<int:pk>/', operacao_grupo.operacao_grupo_delete, name='operacao_grupo_delete'),
    # Operações
    path('<int:cliente>/operacao', operacao.operacao_list, name='operacao_list'),
    path('<int:cliente>/operacao/create', operacao.operacao_create, name='operacao_create'),
    path('<int:cliente>/operacao/update/<int:pk>/', operacao.operacao_update, name='operacao_update'),
    path('<int:cliente>/operacao/delete/<int:pk>/', operacao.operacao_delete, name='operacao_delete'),
    # Manutenções
    path('<int:cliente>/registro-manutencao', registro_manutencao.registro_manutencao_list, name='registro_manutencao_list'),
    path('<int:cliente>/registro-manutencao/create', registro_manutencao.registro_manutencao_create, name='registro_manutencao_create'),
    path('<int:cliente>/registro-manutencao/detail/<int:pk>/', registro_manutencao.registro_manutencao_detail, name='registro_manutencao_detail'),
    path('<int:cliente>/registro-manutencao/update/<int:pk>/', registro_manutencao.registro_manutencao_update, name='registro_manutencao_update'),
    path('<int:cliente>/registro-manutencao/delete/<int:pk>/', registro_manutencao.registro_manutencao_delete, name='registro_manutencao_delete'),
    # Mediçoes
    path('<int:cliente>/medicoes/<int:manutencao>/all', medicoes.all_medicoes, name='all_medicoes'),
    path('<int:cliente>/medicoes/<int:manutencao>/save', medicoes.save_medicoes, name='save_medicoes'),
    path('<int:cliente>/medicoes/<int:manutencao>/save/<int:pk>', medicoes.save_medicoes, name='save_medicoes'),
    path('<int:cliente>/medicoes/<int:manutencao>/delete/<int:pk>', medicoes.delete_medicoes, name='delete_medicoes'),
    # Operações
    path('<int:cliente>/operacoes/<int:manutencao>/grupo-operacao', operacoes.grupo_operacao, name='grupo_operacao'),
    path('<int:cliente>/operacoes/<int:manutencao>/grupo/<int:pk>', operacoes.operacoes, name='operacoes'),
    path('<int:cliente>/operacoes/<int:manutencao>/all', operacoes.all_manutencao_operacao, name='all_manutencao_operacao'),
    path('<int:cliente>/operacoes/<int:manutencao>/save', operacoes.save_manutencao_operacao, name='save_manutencao_operacao'),
    path('<int:cliente>/operacoes/<int:manutencao>/delete/<int:pk>', operacoes.delete_manutencao_operacao, name='delete_manutencao_operacao'),
    # Equipamento Anexos
    path('<int:cliente>/equipamento-anexo/<int:equipamento>/list', equipamento_anexo.equipamento_anexo_list, name='equipamento_anexo_list'),
    path('<int:cliente>/equipamento-anexo/<int:equipamento>/create', equipamento_anexo.equipamento_anexo_create, name='equipamento_anexo_create'),
    path('<int:cliente>/equipamento-anexo/<int:equipamento>/delete/<int:pk>', equipamento_anexo.equipamento_anexo_delete, name='equipamento_anexo_delete'),
    # Equipamento Anexos
    path('<int:cliente>/registro-manutencao-anexo/<int:manutencao>/list', registro_manutencao_anexo.registro_manutencao_anexo_list, name='registro_manutencao_anexo_list'),
    path('<int:cliente>/registro-manutencao-anexo/<int:manutencao>/create', registro_manutencao_anexo.registro_manutencao_anexo_create, name='registro_manutencao_anexo_create'),
    path('<int:cliente>/registro-manutencao-anexo/<int:manutencao>/delete/<int:pk>', registro_manutencao_anexo.registro_manutencao_anexo_delete, name='registro_manutencao_anexo_delete'),
    # Anexo
    path('<int:cliente>/anexo', anexo.anexo_list, name='anexo_list'),
    path('<int:cliente>/anexo/create', anexo.anexo_create, name='anexo_create'),
    path('<int:cliente>/anexo/update/<int:pk>/', anexo.anexo_update, name='anexo_update'),
    path('<int:cliente>/anexo/delete/<int:pk>/', anexo.anexo_delete, name='anexo_delete'),
    # Relatórios
    path('<int:cliente>/relatorios', relatorios.relatorios, name='relatorios'),
    path('<int:cliente>/relatorios/pmoc', relatorios.relatorio_pmoc, name='relatorio_pmoc')
]