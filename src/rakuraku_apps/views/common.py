
from django.shortcuts import get_object_or_404

from django.urls import reverse_lazy

from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate


from rakuraku_apps.forms.common import LoginForm, SignUpForm


class HomeView(TemplateView):
    template_name = 'home.html'

class CustomLoginView(BaseLoginView):
    template_name = 'login.html'    
    form_class = LoginForm
    template_name = "login.html"

class SignupView(CreateView):
    form_class = SignUpForm # 作成した登録用フォームを設定
    template_name = "signup.html" 
    success_url = reverse_lazy("rakuraku_apps:login") # ユーザー作成後のリダイレクト先ページ

    def form_valid(self, form):
        # ユーザー作成後にそのままログイン状態にする設定
        response = super().form_valid(form)
        account_id = form.cleaned_data.get("account_id")
        password = form.cleaned_data.get("password1")
        user = authenticate(account_id=account_id, password=password)
        login(self.request, user)
        return response
    
# LogoutViewを追加
class LogoutView(BaseLogoutView):
    success_url = reverse_lazy("accounts:index")

class EverydayOrIntervalView(TemplateView):
    template_name = 'input/evryday_or_interval.html'