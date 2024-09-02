from datetime import date, datetime

from django.views.generic import TemplateView
from django.shortcuts import redirect
from rakuraku_apps.models import TankModel, WaterQualityModel, WaterQualityThresholdModel
from rakuraku_apps.forms.input import WaterQualityForm
from django.views.generic import TemplateView
from django.shortcuts import redirect
from rakuraku_apps.models import TankModel, WaterQualityModel, WaterQualityThresholdModel
from rakuraku_apps.forms.input import WaterQualityForm
from datetime import datetime, timedelta
# import requests


class EverydayOrIntervalView(TemplateView):
    template_name = 'input/evryday_or_interval.html'



class EverydayFirstInputView(TemplateView):
    template_name = 'input/everyday/first_input.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        print("context",context)
        
        context['tanks'] = TankModel.objects.all()
        today = date.today()
        context['today'] = today.strftime('%Y-%m-%d')
        # context['amedama'] = 'amedamaとは？'

        # その日の日付のデータがすでに存在する場合は、そのデータを初期値として設定
        water_qualities = WaterQualityModel.objects.filter(date=today)
        if water_qualities.exists():
            context['initial_data'] = []
            for water_quality in water_qualities:
                context['initial_data'].append({
                    'tank': water_quality.tank.id,
                    'room_temperature': water_quality.room_temperature,
                    'water_temperature': water_quality.water_temperature,
                    'pH': water_quality.pH,
                    'DO': water_quality.DO,
                    'salinity': water_quality.salinity,
                    'notes': water_quality.notes,
                })

        return context

    def post(self, request, *args, **kwargs):
        date_str = request.POST['date']
        tank_id = request.POST['tank']
        room_temperature = request.POST['room_temperature']
        water_qualities = WaterQualityModel.objects.filter(date=date_str, tank_id=tank_id)
        if water_qualities.exists():
            water_quality = water_qualities.first()
            request.session['water_quality_id'] = water_quality.id
            
            request.session['date'] = water_quality.date.strftime('%Y-%m-%d')
            request.session['tank'] = water_quality.tank_id
            request.session['room_temperature'] = room_temperature
            
            request.session['water_temperature'] = water_quality.water_temperature or ''
            request.session['pH'] = water_quality.pH or ''
            request.session['DO'] = water_quality.DO or ''
            request.session['salinity'] = water_quality.salinity or ''
            
            request.session['notes'] = water_quality.notes or ''
        else:
            request.session['water_quality_id'] = None
            
            request.session['date'] = date_str
            request.session['tank'] = tank_id
            request.session['room_temperature'] = room_temperature
            
            request.session['water_temperature'] = ''
            request.session['pH'] = ''
            request.session['DO'] = ''
            request.session['salinity'] = ''
            
            request.session['notes'] = ''
        return redirect('/everyday/second_input/')

class EverydaySecondInputView(TemplateView):
    template_name = 'input/everyday/second_input.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_data'] = {
            'water_temperature': self.request.session.get('water_temperature', ''),
            'pH': self.request.session.get('pH', ''),
            'DO': self.request.session.get('DO', ''),
            'salinity': self.request.session.get('salinity', ''),
        }
        return context

    def post(self, request, *args, **kwargs):
        request.session['water_temperature'] = request.POST['water_temperature']
        request.session['pH'] = request.POST['pH']
        request.session['DO'] = request.POST['DO']
        request.session['salinity'] = request.POST['salinity']
        return redirect('/everyday/comment/')



class EverydayCommentInputView(TemplateView):
    template_name = 'input/everyday/comment_input.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_data'] = {
            'notes': self.request.session.get('notes', ''),
        }
        return context

    def post(self, request, *args, **kwargs):
        request.session['notes'] = request.POST['notes']
        return redirect('/everyday/confirm/')


class EverydayConfirmInputView(TemplateView):
    template_name = 'input/everyday/confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tank_id = self.request.session.get('tank', '')
        tank = TankModel.objects.get(pk=tank_id)
        date = self.request.session.get('date', '')
        
        form_data = {
            'date': date,
            'tank': tank.name,
            'room_temperature': self.request.session.get('room_temperature', ''),
            'water_temperature': self.request.session.get('water_temperature', ''),
            'pH': self.request.session.get('pH', ''),
            'DO': self.request.session.get('DO', ''),
            'salinity': self.request.session.get('salinity', ''),
            'notes': self.request.session.get('notes', ''),
        }
        context['form_data'] = form_data
        
        # アラートメッセージと背景色を格納する辞書を初期化
        alerts = {}
        bg_colors = {}
        
        # 基準値の範囲内にあるかどうかを確認
        for param in ['water_temperature', 'pH', 'DO', 'salinity']:
            threshold = WaterQualityThresholdModel.objects.filter(parameter=param).first()
            if threshold:
                value = form_data.get(param)
                if value:
                    if threshold.reference_value_threshold_min and float(value) < threshold.reference_value_threshold_min:
                        diff = threshold.reference_value_threshold_min - float(value)
                        alerts.setdefault(param, []).append(f"基準値より{diff:.1f}↓")
                        bg_colors[param] = 'table-warning'
                    elif threshold.reference_value_threshold_max and float(value) > threshold.reference_value_threshold_max:
                        diff = float(value) - threshold.reference_value_threshold_max
                        alerts.setdefault(param, []).append(f"基準値より{diff:.1f}↑")
                        bg_colors[param] = 'table-warning'
        
        # 前日の値から大きく離れているかどうかを確認
        previous_day = datetime.strptime(date, '%Y-%m-%d').date() - timedelta(days=1)
        previous_water_quality = WaterQualityModel.objects.filter(date=previous_day, tank=tank).first()
        if previous_water_quality:
            for param in ['water_temperature', 'pH', 'DO', 'salinity']:
                threshold = WaterQualityThresholdModel.objects.filter(parameter=param).first()
                if threshold and threshold.previous_day_threshold:
                    current_value = form_data.get(param)
                    previous_value = getattr(previous_water_quality, param)
                    if current_value and previous_value:
                        diff = float(current_value) - previous_value
                        if abs(diff) > threshold.previous_day_threshold:
                            if diff > 0:
                                alerts.setdefault(param, []).append(f"前日より{diff:.1f}↑")
                            else:
                                alerts.setdefault(param, []).append(f"前日より{abs(diff):.1f}↓")
                            if param in bg_colors:
                                bg_colors[param] = 'table-danger'
                            else:
                                bg_colors[param] = 'table-warning'
        
        context['alerts'] = alerts
        context['bg_colors'] = bg_colors
        
        # 昨日、一昨日、一週間前の値を取得
        context['previous_values'] = {}
        for days in [1, 2]:
            previous_date = datetime.strptime(date, '%Y-%m-%d').date() - timedelta(days=days)
            previous_water_quality = WaterQualityModel.objects.filter(date=previous_date, tank=tank).first()
            if previous_water_quality:
                context['previous_values'][days] = {
                    'water_temperature': previous_water_quality.water_temperature,
                    'pH': previous_water_quality.pH,
                    'DO': previous_water_quality.DO,
                    'salinity': previous_water_quality.salinity,
                }
        
        return context

    def post(self, request, *args, **kwargs):
        form_data = {
            'date': request.session['date'],
            'tank': request.session['tank'],
            'room_temperature': request.session['room_temperature'],
            'water_temperature': request.session['water_temperature'],
            'pH': request.session['pH'],
            'DO': request.session['DO'],
            'salinity': request.session['salinity'],
            'notes': request.session['notes'],
        }

        water_quality_id = request.session.get('water_quality_id')
        if water_quality_id:
            water_quality = WaterQualityModel.objects.get(id=water_quality_id)
            form = WaterQualityForm(form_data, instance=water_quality)
        else:
            form = WaterQualityForm(form_data)

        if form.is_valid():
            form.save()

            request.session.pop('water_quality_id', None)
            request.session.pop('date', None)
            request.session.pop('tank', None)
            request.session.pop('room_temperature', None)
            request.session.pop('water_temperature', None)
            request.session.pop('pH', None)
            request.session.pop('DO', None)
            request.session.pop('salinity', None)
            request.session.pop('notes', None)
            request.session['success_message'] = '測定結果を保存しました'
            return redirect('/home/')
        else:
            return redirect('/everyday/edit/')


class EverydayEditView(TemplateView):
    template_name = 'input/everyday/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = WaterQualityForm(initial={
            'date': self.request.session.get('date', ''),
            'tank': self.request.session.get('tank', ''),
            'room_temperature': self.request.session.get('room_temperature', ''),
            'water_temperature': self.request.session.get('water_temperature', ''),
            'pH': self.request.session.get('pH', ''),
            'DO': self.request.session.get('DO', ''),
            'salinity': self.request.session.get('salinity', ''),
            'notes': self.request.session.get('notes', ''),
        })
        return context

    def post(self, request, *args, **kwargs):
        form = WaterQualityForm(request.POST)
        if form.is_valid():
            request.session['date'] = form.cleaned_data['date'].strftime('%Y-%m-%d')
            request.session['tank'] = form.cleaned_data['tank'].pk  # 変更
            request.session['room_temperature'] = form.cleaned_data['room_temperature']
            request.session['water_temperature'] = form.cleaned_data['water_temperature']
            request.session['pH'] = form.cleaned_data['pH']
            request.session['DO'] = form.cleaned_data['DO']
            request.session['salinity'] = form.cleaned_data['salinity']
            request.session['notes'] = form.cleaned_data['notes']
            return redirect('/everyday/confirm/')
        else:
            return self.render_to_response(self.get_context_data(form=form))