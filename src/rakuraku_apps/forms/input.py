from django.forms import ChoiceField, DateField, DateInput, Select

from django import forms

from rakuraku_apps.models import TankModel, WaterQualityModel

class WaterQualityForm(forms.ModelForm):
    date = forms.DateField(label='計測日', widget=forms.DateInput(attrs={'type': 'date'}))
    room_temperature = forms.FloatField(label='室温', min_value=0, max_value=100, required=False, widget=forms.NumberInput(attrs={'step': '0.1'}))
    water_temperature = forms.FloatField(label='水温', min_value=0, max_value=100, required=False, widget=forms.NumberInput(attrs={'step': '0.1'}))
    pH = forms.FloatField(label='pH', min_value=0, max_value=14, required=False, widget=forms.NumberInput(attrs={'step': '0.1'}))
    DO = forms.FloatField(label='DO', min_value=0, max_value=100, required=False, widget=forms.NumberInput(attrs={'step': '0.1'}))
    salinity = forms.FloatField(label='塩分濃度', min_value=0, max_value=100, required=False, widget=forms.NumberInput(attrs={'step': '0.1'}))
    notes = forms.CharField(label='備考', widget=forms.Textarea(attrs={'rows': 4}), required=False)

    class Meta:
        model = WaterQualityModel
        fields = ['date', 'room_temperature', 'water_temperature', 'pH', 'DO', 'salinity', 'notes', 'tank']