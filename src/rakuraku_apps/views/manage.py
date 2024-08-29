import json
from urllib import request
from django.views.generic import TemplateView, ListView
from rakuraku_apps.models import ShrimpModel, TankModel, User, WaterQualityThresholdModel
from rakuraku_apps.forms.manage import UserForm, WaterQualityThresholdForm, TankForm, WarningRangeForm
from django.views.generic import UpdateView
from rakuraku_apps.models import StandardValueModel
from django.shortcuts import render, redirect
from django.views import View
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from django.views import View
from rakuraku_apps.forms.manage import WaterQualityThresholdForm
from rakuraku_apps.models import WaterQualityThresholdModel
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rakuraku_apps.forms.manage import TankForm, ShrimpForm



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

class CreateTankView(CreateView):
    model = TankModel
    form_class = TankForm
    template_name = 'manage/create_tank.html'
    success_url = reverse_lazy('rakuraku_apps:manage_tank')

    def form_valid(self, form):
        tank = form.save(commit=False)
        if not tank.shrimp:
            # shrimp が選択されていない場合はエラーメッセージを表示するなどの処理を行う
            form.add_error('shrimp', '系統を選択してください')
            return self.form_invalid(form)
        return super().form_valid(form)

class CreateShrimpView(CreateView):
    model = ShrimpModel
    form_class = ShrimpForm
    template_name = 'manage/create_shrimp.html'
    success_url = reverse_lazy('rakuraku_apps:manage_tank')


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
        thresholds = {
            threshold.parameter: {
                'reference_value_threshold': threshold.reference_value_threshold,
                'previous_day_threshold': threshold.previous_day_threshold,
            }
            for threshold in WaterQualityThresholdModel.objects.all()
        }
        context = {
            'form': form,
            'thresholds': json.dumps(thresholds),
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
    
    
    
from django.core.management import call_command
from django.http import HttpResponse
from django.views.generic.edit import FormView
from rakuraku_apps.forms.manage import PopulateDBForm, ClearDBForm

class PopulateDBView(FormView):
    template_name = 'manage/populate_db.html'
    form_class = PopulateDBForm
    success_url = reverse_lazy('rakuraku_apps:manage_tank')

    def form_valid(self, form):
        # users = form.cleaned_data.get('users')
        tanks = form.cleaned_data.get('tanks')
        water_quality = form.cleaned_data.get('water_quality')

        # if users:
        #     call_command('populate_db', users=users)
        if tanks:
            call_command('populate_db', tanks=tanks)
        if water_quality:
            call_command('populate_db', wq=water_quality)

        return super().form_valid(form)

class ClearDBView(FormView):
    template_name = 'manage/clear_db.html'
    form_class = ClearDBForm
    success_url = reverse_lazy('rakuraku_apps:manage_tank')

    def form_valid(self, form):
        # users = form.cleaned_data.get('users')
        tanks = form.cleaned_data.get('tanks')
        water_quality = form.cleaned_data.get('water_quality')

        # if users:
        #     call_command('clear_db', users=True)
        if tanks:
            call_command('clear_db', tanks=True)
        if water_quality:
            call_command('clear_db', wq=True)

        return super().form_valid(form)
    
