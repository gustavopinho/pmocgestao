# coding=utf-8

import re

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class User(AbstractUser):

    name = models.CharField('Nome', max_length=255, blank=False)
    email = models.EmailField('E-mail', unique=True, blank=False)

    updated = models.DateTimeField('Modificado em', auto_now=True)

    objects = UserManager()

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        permissions = (
            ("view_userempresa", "Ver usuário da empresa"),
            ("add_userempresa", "Adicionar usuário da empresa"),
            ("change_userempresa", "Alterar usuário da empresa"),
            ("delete_userempresa", "Excluír usuário da empresa"),
        )

    def __str__(self):
        return self.name or self.username

    def checkgroup(self):
        groups = []
        for group in self.groups.all():
            groups.append(group.name)

        return groups
