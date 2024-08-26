from django import forms
from rakuraku_apps.models import StandardValueModel, User
from rakuraku_apps.models import TankModel
from rakuraku_apps.models import StandardValueModel, WaterQualityThresholdModel
from django.core.exceptions import ValidationError

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['account_id']

class TankForm(forms.ModelForm):
    class Meta:
        model = TankModel
        fields = ['name']


class WarningRangeForm(forms.ModelForm):
    class Meta:
        model = StandardValueModel
        fields = [
            'water_temperature',
            'pH',
            'DO',
            'salinity',
            'NH4',
            'NO2',
            'NO3',
            'Ca',
            'Al',
            'Mg',
        ]

class WaterQualityThresholdForm(forms.ModelForm):
    class Meta:
        model = WaterQualityThresholdModel
        fields = ['parameter', 'reference_value_threshold', 'previous_day_threshold']
        labels = {
            'parameter': 'パラメーター',
            'reference_value_threshold': '基準値との差異閾値',
            'previous_day_threshold': '前日との差異閾値',
        }
        widgets = {
            'parameter': forms.Select(attrs={'class': 'form-control'}),
            'reference_value_threshold': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'required': True}),
            'previous_day_threshold': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'required': True}),
        }