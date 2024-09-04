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
    template_name = "login.html"



class SignupView(CreateView):
    form_class = SignUpForm
    template_name = "signup.html" 
    success_url = reverse_lazy("rakuraku_apps:manage_user") # ユーザー作成後のリダイレクト先ページ

    def form_valid(self, form):
        # ユーザー作成後にそのままログイン状態にする設定
        response = super().form_valid(form)
        account_id = form.cleaned_data.get("account_id")
        password = form.cleaned_data.get("password1")
        user = authenticate(account_id=account_id, password=password)
        login(self.request, user)
        return response
    

class LogoutView(BaseLogoutView):
    success_url = reverse_lazy("accounts:index")


class EverydayOrIntervalView(TemplateView):
    template_name = 'input/evryday_or_interval.html'