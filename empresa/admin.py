from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from .models import (
    Empresa, UsuarioEmpresa, Responsavel, Tecnico,
    EquipamentoGrupo, ManutencaoTipo, ManutencaoIntervalo
)

class EmpresaAdmin(GuardedModelAdmin):
    pass

admin.site.register(Empresa, EmpresaAdmin)
admin.site.register([
    UsuarioEmpresa, Responsavel, Tecnico,
    EquipamentoGrupo, ManutencaoTipo, ManutencaoIntervalo
])