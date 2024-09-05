from django.urls import reverse_lazy

from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate

from rakuraku_apps.forms.common import LoginForm, SignUpForm


class HomeView(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success_message'] = self.request.session.pop('success_message', None)
        return context



class CustomLoginView(BaseLoginView):
    template_name = 'login.html'    
    form_class = LoginForm



class SignupView(CreateView):
    form_class = SignUpForm
    template_name = "signup.html" 
    success_url = reverse_lazy("rakuraku_apps:manage_user") # ユーザー作成後のリダイレクト先ページ
    

class LogoutView(BaseLogoutView):
    success_url = reverse_lazy("accounts:index")


class EverydayOrIntervalView(TemplateView):
    template_name = 'input/evryday_or_interval.html'

class FunctionView(TemplateView):
    template_name = 'function.html'

class OmakeView(TemplateView):
    template_name = 'omake.html'

class Omake1View(TemplateView):
    template_name = 'omake/omake1.html'

class Omake2View(TemplateView):
    template_name = 'omake/omake2.html'

class Omake3View(TemplateView):
    template_name = 'omake/omake3.html'

class Omake4View(TemplateView):
    template_name = 'omake/omake4.html'

class Omake5View(TemplateView):
    template_name = 'omake/omake5.html'

class Omake6View(TemplateView):
    template_name = 'omake/omake6.html'

class Omake7View(TemplateView):
    template_name = 'omake/omake7.html'

class Omake8View(TemplateView):
    template_name = 'omake/omake8.html'

class Omake9View(TemplateView):
    template_name = 'omake/omake9.html'

class Omake10View(TemplateView):
    template_name = 'omake/omake10.html'