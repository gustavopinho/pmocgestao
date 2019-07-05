from datetime import date

from django.db.models import FileField
from django.forms import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

class ContentTypeRestrictedFileField(FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB 104857600
            250MB - 214958080
            500MB - 429916160
    """
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop('content_types', [])
        self.max_upload_size = kwargs.pop('max_upload_size', 0)

        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):        
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)
        
        file = data.file
        try:
            content_type = file.content_type
            if content_type in self.content_types:
                if file._size > self.max_upload_size:
                    raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(self.max_upload_size), filesizeformat(file._size)))
            else:
                raise forms.ValidationError(_('Filetype not supported.'))
        except AttributeError:
            pass        
            
        return data

def get_empresa(request, pk):
    """Retorna a empresa de acordo com o usuário logado"""
    empresa_usuario = request.user.empresas.get(empresa__pk=pk)
    return empresa_usuario.empresa


class Month():
    
    month_date = date(2000, 1, 1)

    def __init__(self, year, month):
        self.month_date = date(int(year), int(month), 1)

    def get_month_name(self):

        months = {
            1 : 'Janeiro',
            2 : 'Fevereiro',
            3 : 'Março',
            4 : 'Abril',
            5 : 'Maio',
            6 : 'Junho',
            7 : 'Julho',
            8 : 'Agosto',
            9 : 'Setembro',
            10 : 'Outubro',
            11 : 'Novembro',
            12 : 'Dezembro',
        }

        return months[self.month_date.month];

    def get_short_name(self):
        return self.get_month_name()[:3];

    def get_short(self):
        return "{0}/{1}".format(self.month_date.month, self.month_date.year)

    def __str__(self):
        return self.get_month_name();