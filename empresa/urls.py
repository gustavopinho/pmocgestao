from django.urls import include, path, reverse_lazy
from django.views.generic import RedirectView

from . import views

app_name = 'empresa'
urlpatterns = [
    # Dashboard
    path('<int:pk>/dashboard', views.empresa_dashboard, name='empresa_dashboard'),
    path('<int:pk>/dashboard/relatorios', views.empresa_relatorios, name='empresa_relatorios'),
    # Empresa
    path('create/', views.empresa_create, name='empresa_create'),
    path('update/<int:pk>/', views.empresa_update, name='empresa_update'),
    # Grupo de equipamentos
    path('<int:empresa>/equipamento-grupo', views.equipamento_grupo_list, name='equipamento_grupo_list'),
    path('<int:empresa>/equipamento-grupo/create', views.equipamento_grupo_create, name='equipamento_grupo_create'),
    path('<int:empresa>/equipamento-grupo/update/<int:pk>/', views.equipamento_grupo_update, name='equipamento_grupo_update'),
    path('<int:empresa>/equipamento-grupo/delete/<int:pk>/', views.equipamento_grupo_delete, name='equipamento_grupo_delete'),
    # Tipo de manutenção 
    path('<int:empresa>/manutencao-tipo', views.manutencao_tipo_list, name='manutencao_tipo_list'),
    path('<int:empresa>/manutencao-tipo/create', views.manutencao_tipo_create, name='manutencao_tipo_create'),
    path('<int:empresa>/manutencao-tipo/update/<int:pk>/', views.manutencao_tipo_update, name='manutencao_tipo_update'),
    path('<int:empresa>/manutencao-tipo/delete/<int:pk>/', views.manutencao_tipo_delete, name='manutencao_tipo_delete'),
    # Intervalo de manutenção 
    path('<int:empresa>/manutencao-intervalo', views.manutencao_intervalo_list, name='manutencao_intervalo_list'),
    path('<int:empresa>/manutencao-intervalo/create', views.manutencao_intervalo_create, name='manutencao_intervalo_create'),
    path('<int:empresa>/manutencao-intervalo/update/<int:pk>/', views.manutencao_intervalo_update, name='manutencao_intervalo_update'),
    path('<int:empresa>/manutencao-intervalo/delete/<int:pk>/', views.manutencao_intervalo_delete, name='manutencao_intervalo_delete'),
    # Responsavel técnico
    path('<int:empresa>/responsavel', views.responsavel_list, name='responsavel_list'),
    path('<int:empresa>/responsavel/create', views.responsavel_create, name='responsavel_create'),
    path('<int:empresa>/responsavel/update/<int:pk>/', views.responsavel_update, name='responsavel_update'),
    path('<int:empresa>/responsavel/delete/<int:pk>/', views.responsavel_delete, name='responsavel_delete'),
    # Técnico
    path('<int:empresa>/tecnico', views.tecnico_list, name='tecnico_list'),
    path('<int:empresa>/tecnico/create', views.tecnico_create, name='tecnico_create'),
    path('<int:empresa>/tecnico/update/<int:pk>/', views.tecnico_update, name='tecnico_update'),
    path('<int:empresa>/tecnico/delete/<int:pk>/', views.tecnico_delete, name='tecnico_delete'),
    # Usuário
    path('<int:empresa>/usuario', views.user_list, name='user_list'),
    path('<int:empresa>/usuario/create', views.user_create, name='user_create'),
    path('<int:empresa>/usuario/update/<int:pk>/', views.user_update, name='user_update'),
    path('<int:empresa>/usuario/update-password/<int:pk>/', views.user_update_password, name='user_update_password'),
    path('<int:empresa>/usuario/delete/<int:pk>/', views.user_delete, name='user_delete'),
    path('<int:empresa>/usuario/<int:usuario>/gerar-acesso/', views.user_gerar_acesso, name='user_gerar_acesso'),
    path('<int:empresa>/cliente/', include('cliente.urls', namespace='cliente')),
]