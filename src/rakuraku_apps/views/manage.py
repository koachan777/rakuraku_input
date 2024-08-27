from urllib import request
from django.views.generic import TemplateView, ListView
from rakuraku_apps.models import TankModel, User, WaterQualityThresholdModel
from rakuraku_apps.forms.manage import UserForm, WaterQualityThresholdForm, TankForm, WarningRangeForm
from django.views.generic import UpdateView
from rakuraku_apps.models import StandardValueModel
from django.shortcuts import render, redirect
from django.views import View


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



class ManageValueView(UpdateView):
    model = StandardValueModel
    form_class = WarningRangeForm
    template_name = 'manage/value.html'
    success_url = '/manage/'

    def get_object(self, queryset=None):
        return StandardValueModel.get_or_create()
    



class ManageAlertView(View):
    def get(self, request):
        form = WaterQualityThresholdForm()
        context = {
            'form': form,
        }
        return render(request, 'manage/alert.html', context)

    def post(self, request):
        form = WaterQualityThresholdForm(request.POST)
        if form.is_valid():
            parameter = form.cleaned_data['parameter']
            reference_value_threshold = form.cleaned_data['reference_value_threshold']
            previous_day_threshold = form.cleaned_data['previous_day_threshold']

            threshold, created = WaterQualityThresholdModel.objects.update_or_create(
                parameter=parameter,
                defaults={
                    'reference_value_threshold': reference_value_threshold,
                    'previous_day_threshold': previous_day_threshold,
                }
            )

            return redirect('/manage/')

        context = {
            'form': form,
        }
        return render(request, 'manage/alert.html', context)