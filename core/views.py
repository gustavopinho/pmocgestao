from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

class DashBoardView(LoginRequiredMixin, View):
    template_name = 'dashboard.html'

    def get(self, request):
        return render(request, self.template_name, {})

dashboard = DashBoardView.as_view()
