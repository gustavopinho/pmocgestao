from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from . import views

app_name = 'core'
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('favicon.ico', RedirectView.as_view(url='/static/img/favicon.ico', permanent=True)),
    path('', RedirectView.as_view(url=reverse_lazy('core:dashboard'), permanent=False)),
]