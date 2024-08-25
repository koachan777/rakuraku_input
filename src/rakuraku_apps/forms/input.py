from django.forms import ChoiceField, DateField, DateInput, Select

from django import forms

from rakuraku_apps.models import TankModel, WaterQualityModel

class WaterQualityForm(forms.ModelForm):
    date = forms.DateField(label='計測日', widget=forms.DateInput(attrs={'type': 'date'}))
    room_temperature = forms.IntegerField(label='室温', min_value=0, max_value=100, required=False)
    water_temperature = forms.IntegerField(label='水温', min_value=0, max_value=100, required=False)
    pH = forms.IntegerField(label='pH', min_value=0, max_value=14, required=False)
    DO = forms.IntegerField(label='DO', min_value=0, max_value=100, required=False)
    salinity = forms.IntegerField(label='塩分濃度', min_value=0, max_value=100, required=False)
    notes = forms.CharField(label='備考', widget=forms.Textarea(attrs={'rows': 4}), required=False)

    class Meta:
        model = WaterQualityModel
        fields = ['date', 'room_temperature', 'water_temperature', 'pH', 'DO', 'salinity', 'notes', 'tank']