from urllib import request

from django.views.generic import TemplateView, ListView, CreateView, DeleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Prefetch, Count
from django.contrib.auth.mixins import UserPassesTestMixin

from rakuraku_apps.models import ShrimpModel, TankModel, User, WaterQualityThresholdModel
from rakuraku_apps.forms.manage import UserForm, WaterQualityThresholdForm, TankForm, WaterQualityThresholdForm, ShrimpForm
from rakuraku_apps.models import WaterQualityThresholdModel


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
    


class DeleteUserView(UserPassesTestMixin, DeleteView):
    model = User
    success_url = reverse_lazy('rakuraku_apps:manage_user')
    template_name = None

    def test_func(self):
        user = self.get_object()
        return user != self.request.user



class ManageTankView(ListView):
    model = TankModel
    template_name = 'manage/tank.html'
    context_object_name = 'shrimps'

    def get_queryset(self):
        return ShrimpModel.objects.annotate(
            tank_count=Count('tank')
        ).filter(
            tank_count__gt=0
        ).prefetch_related(
            Prefetch('tank', queryset=TankModel.objects.order_by('name'))
        )
    


class DeleteTankView(DeleteView):
    model = TankModel
    success_url = reverse_lazy('rakuraku_apps:manage_tank')
    template_name = None

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.water_quality.all().delete()  # 関連する水質データを削除
        return super().delete(request, *args, **kwargs)



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



class ManageValueView(TemplateView):
    template_name = 'manage/value.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = WaterQualityThresholdForm(initial={
            'water_temperature_max': getattr(WaterQualityThresholdModel.objects.filter(parameter='water_temperature').first(), 'reference_value_threshold_max', None),
            'water_temperature_min': getattr(WaterQualityThresholdModel.objects.filter(parameter='water_temperature').first(), 'reference_value_threshold_min', None),
            'water_temperature_diff': getattr(WaterQualityThresholdModel.objects.filter(parameter='water_temperature').first(), 'previous_day_threshold', None),
            'pH_max': getattr(WaterQualityThresholdModel.objects.filter(parameter='pH').first(), 'reference_value_threshold_max', None),
            'pH_min': getattr(WaterQualityThresholdModel.objects.filter(parameter='pH').first(), 'reference_value_threshold_min', None),
            'pH_diff': getattr(WaterQualityThresholdModel.objects.filter(parameter='pH').first(), 'previous_day_threshold', None),
            'DO_max': getattr(WaterQualityThresholdModel.objects.filter(parameter='DO').first(), 'reference_value_threshold_max', None),
            'DO_min': getattr(WaterQualityThresholdModel.objects.filter(parameter='DO').first(), 'reference_value_threshold_min', None),
            'DO_diff': getattr(WaterQualityThresholdModel.objects.filter(parameter='DO').first(), 'previous_day_threshold', None),
            'salinity_max': getattr(WaterQualityThresholdModel.objects.filter(parameter='salinity').first(), 'reference_value_threshold_max', None),
            'salinity_min': getattr(WaterQualityThresholdModel.objects.filter(parameter='salinity').first(), 'reference_value_threshold_min', None),
            'salinity_diff': getattr(WaterQualityThresholdModel.objects.filter(parameter='salinity').first(), 'previous_day_threshold', None),
            'NH4_max': getattr(WaterQualityThresholdModel.objects.filter(parameter='NH4').first(), 'reference_value_threshold_max', None),
            'NH4_min': getattr(WaterQualityThresholdModel.objects.filter(parameter='NH4').first(), 'reference_value_threshold_min', None),
            'NH4_diff': getattr(WaterQualityThresholdModel.objects.filter(parameter='NH4').first(), 'previous_day_threshold', None),
            'NO2_max': getattr(WaterQualityThresholdModel.objects.filter(parameter='NO2').first(), 'reference_value_threshold_max', None),
            'NO2_min': getattr(WaterQualityThresholdModel.objects.filter(parameter='NO2').first(), 'reference_value_threshold_min', None),
            'NO2_diff': getattr(WaterQualityThresholdModel.objects.filter(parameter='NO2').first(), 'previous_day_threshold', None),
            'NO3_max': getattr(WaterQualityThresholdModel.objects.filter(parameter='NO3').first(), 'reference_value_threshold_max', None),
            'NO3_min': getattr(WaterQualityThresholdModel.objects.filter(parameter='NO3').first(), 'reference_value_threshold_min', None),
            'NO3_diff': getattr(WaterQualityThresholdModel.objects.filter(parameter='NO3').first(), 'previous_day_threshold', None),
            'Ca_max': getattr(WaterQualityThresholdModel.objects.filter(parameter='Ca').first(), 'reference_value_threshold_max', None),
            'Ca_min': getattr(WaterQualityThresholdModel.objects.filter(parameter='Ca').first(), 'reference_value_threshold_min', None),
            'Ca_diff': getattr(WaterQualityThresholdModel.objects.filter(parameter='Ca').first(), 'previous_day_threshold', None),
            'Al_max': getattr(WaterQualityThresholdModel.objects.filter(parameter='Al').first(), 'reference_value_threshold_max', None),
            'Al_min': getattr(WaterQualityThresholdModel.objects.filter(parameter='Al').first(), 'reference_value_threshold_min', None),
            'Al_diff': getattr(WaterQualityThresholdModel.objects.filter(parameter='Al').first(), 'previous_day_threshold', None),
            'Mg_max': getattr(WaterQualityThresholdModel.objects.filter(parameter='Mg').first(), 'reference_value_threshold_max', None),
            'Mg_min': getattr(WaterQualityThresholdModel.objects.filter(parameter='Mg').first(), 'reference_value_threshold_max', None),
            'Mg_diff': getattr(WaterQualityThresholdModel.objects.filter(parameter='Mg').first(), 'previous_day_threshold', None),
        })
        return context

    def post(self, request, *args, **kwargs):
        form = WaterQualityThresholdForm(request.POST)
        if form.is_valid():
            WaterQualityThresholdModel.update_or_create('water_temperature', form.cleaned_data['water_temperature_max'], form.cleaned_data['water_temperature_min'], form.cleaned_data['water_temperature_diff'])
            WaterQualityThresholdModel.update_or_create('pH', form.cleaned_data['pH_max'], form.cleaned_data['pH_min'], form.cleaned_data['pH_diff'])
            WaterQualityThresholdModel.update_or_create('DO', form.cleaned_data['DO_max'], form.cleaned_data['DO_min'], form.cleaned_data['DO_diff'])
            WaterQualityThresholdModel.update_or_create('salinity', form.cleaned_data['salinity_max'], form.cleaned_data['salinity_min'], form.cleaned_data['salinity_diff'])
            WaterQualityThresholdModel.update_or_create('NH4', form.cleaned_data['NH4_max'],form.cleaned_data['NH4_min'], form.cleaned_data['NH4_diff'])
            WaterQualityThresholdModel.update_or_create('NO2', form.cleaned_data['NO2_max'], form.cleaned_data['NO2_min'], form.cleaned_data['NO2_diff'])
            WaterQualityThresholdModel.update_or_create('NO3', form.cleaned_data['NO3_max'], form.cleaned_data['NO3_min'], form.cleaned_data['NO3_diff'])
            WaterQualityThresholdModel.update_or_create('Ca', form.cleaned_data['Ca_max'], form.cleaned_data['Ca_min'], form.cleaned_data['Ca_diff'])
            WaterQualityThresholdModel.update_or_create('Al', form.cleaned_data['Al_max'], form.cleaned_data['Al_min'], form.cleaned_data['Al_diff'])
            WaterQualityThresholdModel.update_or_create('Mg', form.cleaned_data['Mg_max'], form.cleaned_data['Mg_min'], form.cleaned_data['Mg_diff'])
            return redirect('rakuraku_apps:manage')
        return self.render_to_response(self.get_context_data(form=form))