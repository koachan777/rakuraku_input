from django import forms
from rakuraku_apps.models import ShrimpModel, User, TankModel
from rakuraku_apps.models import TankModel


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['account_id']


class TankForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shrimp'].queryset = ShrimpModel.objects.all()
        self.fields['shrimp'].label_from_instance = lambda obj: obj.family

    class Meta:
        model = TankModel
        fields = ['name', 'shrimp']


class ShrimpForm(forms.ModelForm):
    class Meta:
        model = ShrimpModel
        fields = ['family']


class WaterQualityThresholdForm(forms.Form):
    water_temperature_min = forms.FloatField(label='水温の下限値', required=False)
    water_temperature_max = forms.FloatField(label='水温の上限値', required=False)
    water_temperature_diff = forms.FloatField(label='水温の前日差異閾値', required=False)
    pH_min = forms.FloatField(label='pHの下限値', required=False)
    pH_max = forms.FloatField(label='pHの上限値', required=False)
    pH_diff = forms.FloatField(label='pHの前日差異閾値', required=False)
    DO_min = forms.FloatField(label='DOの下限値', required=False)
    DO_max = forms.FloatField(label='DOの上限値', required=False)
    DO_diff = forms.FloatField(label='DOの前日差異閾値', required=False)
    salinity_min = forms.FloatField(label='塩分濃度の下限値', required=False)
    salinity_max = forms.FloatField(label='塩分濃度の上限値', required=False)
    salinity_diff = forms.FloatField(label='塩分濃度の前日差異閾値', required=False)
    NH4_min = forms.FloatField(label='NH4の下限値', required=False)
    NH4_max = forms.FloatField(label='NH4の上限値', required=False)
    NH4_diff = forms.FloatField(label='NH4の前日差異閾値', required=False)
    NO2_min = forms.FloatField(label='NH4の下限値', required=False)
    NO2_max = forms.FloatField(label='NO2の上限値', required=False)
    NO2_diff = forms.FloatField(label='NO2の前日差異閾値', required=False)
    NO3_min = forms.FloatField(label='NO3の下限値', required=False)
    NO3_max = forms.FloatField(label='NO3の上限値', required=False)
    NO3_diff = forms.FloatField(label='NO3の前日差異閾値', required=False)
    Ca_min = forms.FloatField(label='Caの下限値', required=False)
    Ca_max = forms.FloatField(label='Caの上限値', required=False)
    Ca_diff = forms.FloatField(label='Caの前日差異閾値', required=False)
    Al_min = forms.FloatField(label='Alの下限値', required=False)
    Al_max = forms.FloatField(label='Alの上限値', required=False)
    Al_diff = forms.FloatField(label='Alの前日差異閾値', required=False)
    Mg_min = forms.FloatField(label='Mgの下限値', required=False)
    Mg_max = forms.FloatField(label='Mgの上限値', required=False)
    Mg_diff = forms.FloatField(label='Mgの前日差異閾値', required=False)