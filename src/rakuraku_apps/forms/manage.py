from django import forms
from rakuraku_apps.models import User
from rakuraku_apps.models import TankModel


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['account_id']

class TankForm(forms.ModelForm):
    class Meta:
        model = TankModel
        fields = ['name']