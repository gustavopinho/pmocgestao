from django.urls import include, path 
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.contrib.auth.views import login, logout
from django.conf.urls.static import static

from django.contrib.auth.views import (
    password_reset, password_reset_done,
    password_reset_confirm, password_reset_complete
)


urlpatterns = [
    path('', include('core.urls', namespace='core')),
    path('empresa/', include('empresa.urls', namespace='empresa')),
    path('conta/', include('accounts.urls', namespace='accounts')),
    path('entrar/', login, {'template_name': 'login.html'}, name='login'),
    path('sair/', logout, {'next_page': 'login'}, name='logout'),
    path('admin/', admin.site.urls),

    path('esqueci-minha-senha/', password_reset, {
        'template_name': 'password_reset_form.html',
        'html_email_template_name': 'password_reset_email.html',
        'subject_template_name': 'password_reset_subject.txt'
    }, name='password_reset'),
    path('esqueci-minha-senha/completo/', password_reset_done, {
        'template_name': 'password_reset_done.html'
    }, name='password_reset_done'),
    path('esqueci-minha-senha/<uidb64>/<token>/', password_reset_confirm, {
        'template_name': 'password_reset_confirm.html'
    },name='password_reset_confirm'),
    path('esqueci-minha-senha/finalizado/', password_reset_complete, {
        'template_name': 'password_reset_complete.html'
    }, name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )