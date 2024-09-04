from django import forms
from rakuraku_apps.models import TankModel, WaterQualityModel


class WaterQualityEditForm(forms.ModelForm):
    date = forms.DateField(label='計測日', widget=forms.DateInput(attrs={'type': 'date', 'readonly': 'readonly'}))
    room_temperature = forms.FloatField(label='室温', min_value=0, max_value=100, required=False, widget=forms.NumberInput(attrs={'step': '0.1'}))
    water_temperature = forms.FloatField(label='水温', min_value=0, max_value=100, required=False, widget=forms.NumberInput(attrs={'step': '0.1'}))
    pH = forms.FloatField(label='pH', min_value=0, max_value=14, required=False, widget=forms.NumberInput(attrs={'step': '0.01'}))
    DO = forms.FloatField(label='DO', min_value=0, max_value=100, required=False, widget=forms.NumberInput(attrs={'step': '0.1'}))
    salinity = forms.FloatField(label='塩分濃度', min_value=0, max_value=100, required=False, widget=forms.NumberInput(attrs={'step': '0.01'}))
    NH4 = forms.FloatField(label='NH4', min_value=0, max_value=100, required=False, widget=forms.NumberInput(attrs={'step': '0.1'}))
    NO2 = forms.FloatField(label='NO2', min_value=0, max_value=100, required=False, widget=forms.NumberInput(attrs={'step': '0.1'}))
    NO3 = forms.FloatField(label='NO3', min_value=0, max_value=100, required=False, widget=forms.NumberInput(attrs={'step': '1'}))
    Ca = forms.FloatField(label='Ca', min_value=0, max_value=500, required=False, widget=forms.NumberInput(attrs={'step': '1'}))
    Al = forms.FloatField(label='Al', min_value=0, max_value=300, required=False, widget=forms.NumberInput(attrs={'step': '1'}))
    Mg = forms.FloatField(label='Mg', min_value=0, max_value=1000, required=False, widget=forms.NumberInput(attrs={'step': '1'}))
    notes = forms.CharField(label='備考', widget=forms.Textarea(attrs={'rows': 4}), required=False)

    class Meta:
        model = WaterQualityModel
        fields = ['date', 'room_temperature', 'water_temperature', 'pH', 'DO', 'salinity', 'NH4', 'NO2', 'NO3', 'Ca', 'Al', 'Mg', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['readonly'] = True