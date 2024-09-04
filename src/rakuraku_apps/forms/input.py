from django import forms
from rakuraku_apps.models import TankModel, WaterQualityModel


class WaterQualityForm(forms.ModelForm):
    date = forms.DateField(label='計測日', widget=forms.DateInput(attrs={'type': 'date'}))
    room_temperature = forms.FloatField(label='室温', min_value=0, max_value=100, required=False, widget=forms.NumberInput(attrs={'step': '0.1'}))
    water_temperature = forms.FloatField(label='水温', min_value=0, max_value=100, required=False, widget=forms.NumberInput(attrs={'step': '0.1'}))
    pH = forms.FloatField(label='pH', min_value=0, max_value=14, required=False, widget=forms.NumberInput(attrs={'step': '0.01'}))
    DO = forms.FloatField(label='DO', min_value=0, max_value=100, required=False, widget=forms.NumberInput(attrs={'step': '0.1'}))
    salinity = forms.FloatField(label='塩分濃度', min_value=0, max_value=100, required=False, widget=forms.NumberInput(attrs={'step': '0.01'}))
    notes = forms.CharField(label='備考', widget=forms.Textarea(attrs={'rows': 4}), required=False)
    tank = forms.ModelChoiceField(
        queryset=TankModel.objects.all(),
        label='水槽',
        widget=forms.Select(),
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tank'].label_from_instance = lambda obj: obj.name
        
    class Meta:
        model = WaterQualityModel
        fields = ['date', 'room_temperature', 'water_temperature', 'pH', 'DO', 'salinity', 'notes', 'tank']

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        tank = cleaned_data.get('tank')

        if date and tank:
            try:
                water_quality = WaterQualityModel.objects.get(date=date, tank=tank)
                self.instance = water_quality
            except WaterQualityModel.DoesNotExist:
                pass

        return cleaned_data
    
    
class IntervalWaterQualityForm(forms.ModelForm):
    date = forms.DateField(label='計測日', widget=forms.DateInput(attrs={'type': 'date'}))
    tank = forms.ModelChoiceField(
        queryset=TankModel.objects.all(),
        label='水槽',
        widget=forms.Select(),
    )
    room_temperature = forms.FloatField(label='室温', min_value=0, max_value=100, required=False, widget=forms.NumberInput(attrs={'step': '0.1'}))
    NH4 = forms.FloatField(label='NH4', min_value=0, max_value=100, required=False, widget=forms.NumberInput(attrs={'step': '0.1'}))
    NO2 = forms.FloatField(label='NO2', min_value=0, max_value=100, required=False, widget=forms.NumberInput(attrs={'step': '0.1'}))
    NO3 = forms.FloatField(label='NO3', min_value=0, max_value=100, required=False, widget=forms.NumberInput(attrs={'step': '1'}))
    Ca = forms.FloatField(label='Ca', min_value=0, max_value=500, required=False, widget=forms.NumberInput(attrs={'step': '1'}))
    Al = forms.FloatField(label='Al', min_value=0, max_value=300, required=False, widget=forms.NumberInput(attrs={'step': '1'}))
    Mg = forms.FloatField(label='Mg', min_value=0, max_value=1000, required=False, widget=forms.NumberInput(attrs={'step': '1'}))
    notes = forms.CharField(label='備考', widget=forms.Textarea(attrs={'rows': 4}), required=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tank'].label_from_instance = lambda obj: obj.name
        
    class Meta:
        model = WaterQualityModel
        fields = ['date', 'tank', 'room_temperature', 'NH4', 'NO2', 'NO3', 'Ca', 'Al', 'Mg', 'notes']

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        tank = cleaned_data.get('tank')

        if date and tank:
            try:
                water_quality = WaterQualityModel.objects.get(date=date, tank=tank)
                self.instance = water_quality
            except WaterQualityModel.DoesNotExist:
                pass

        return cleaned_data