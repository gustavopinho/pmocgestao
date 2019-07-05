# coding=utf-8
import calendar
from datetime import date

from django.template import Library

from cliente.models import RegistroManutencaoOperacao

register = Library()

@register.simple_tag
def operacao(k, i, agenda):
    return agenda[k][i]['exec'];