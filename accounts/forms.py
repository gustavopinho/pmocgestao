# coding=utf-8

from django.contrib.auth.forms import (UserCreationForm, UserChangeForm)

from .models import User

class UserAdminForm(UserChangeForm):

    class Meta:
        model = User
        fields = '__all__'

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'name', 'email']


    def save(self, commit=True):

        user = super(UserCreationForm, self).save(commit=commit)
        user.set_password(self.cleaned_data["password1"])
        user.save()
        
        return user