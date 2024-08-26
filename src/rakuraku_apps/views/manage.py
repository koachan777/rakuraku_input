from django.views.generic import TemplateView
from django.views.generic import ListView
from rakuraku_apps.models import TankModel, User
from rakuraku_apps.forms.manage import UserForm
from rakuraku_apps.forms.manage import TankForm


class ManageView(TemplateView):
    template_name = 'manage/manage.html'

class ManageUserView(ListView):
    model = User
    template_name = 'manage/user.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserForm()
        return context

class ManageTankView(ListView):
    model = TankModel
    template_name = 'manage/tank.html'
    context_object_name = 'tanks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TankForm()
        return context

class ManagValueView(TemplateView):
    template_name = 'manage/value.html'

class ManageFirstAlertView(TemplateView):
    template_name = 'manage/first_alert.html'

class ManageSecondAlertView(TemplateView):
    template_name = 'manage/second_alert.html'