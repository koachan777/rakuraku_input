
from django.shortcuts import get_object_or_404


from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'


class LoginView(TemplateView):
    template_name = 'login.html'

class RegistrationView(TemplateView):
    template_name = 'registration.html'

class EverydayOrIntervalView(TemplateView):
    template_name = 'input/evryday_or_interval.html'