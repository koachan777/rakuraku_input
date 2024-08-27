from datetime import date

from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.views.generic import TemplateView
from rakuraku_apps.models import StandardValueModel, TankModel, WaterQualityModel, WaterQualityThresholdModel
from rakuraku_apps.forms.input import WaterQualityForm


class EverydayOrIntervalView(TemplateView):
    template_name = 'input/evryday_or_interval.html'



class EverydayFirstInputView(TemplateView):
    template_name = 'input/everyday/first_input.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tanks'] = TankModel.objects.all()
        today = date.today()
        context['today'] = today.strftime('%Y-%m-%d')

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
            request.session['room_temperature'] = water_quality.room_temperature or room_temperature
            request.session['water_temperature'] = water_quality.water_temperature or ''
            request.session['pH'] = water_quality.pH or ''
            request.session['DO'] = water_quality.DO or ''
            request.session['salinity'] = water_quality.salinity or ''
            request.session['notes'] = water_quality.notes or ''
        else:
            request.session['date'] = date_str
            request.session['tank'] = tank_id
            request.session['room_temperature'] = room_temperature

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
        context['form_data'] = {
            'date': self.request.session.get('date', ''),
            'tank': tank.name,
            'room_temperature': self.request.session.get('room_temperature', ''),
            'water_temperature': self.request.session.get('water_temperature', ''),
            'pH': self.request.session.get('pH', ''),
            'DO': self.request.session.get('DO', ''),
            'salinity': self.request.session.get('salinity', ''),
            'notes': self.request.session.get('notes', ''),
        }

        # 基準値を取得
        standard_value = StandardValueModel.get_or_create()

        # 閾値を取得
        thresholds = {t.parameter: t for t in WaterQualityThresholdModel.objects.all()}

        # アラートメッセージを格納する辞書
        context['alerts'] = {}

        # 各パラメーターについて基準値と比較
        for param in ['water_temperature', 'pH', 'DO', 'salinity', 'NH4', 'NO2', 'NO3', 'Ca', 'Al', 'Mg']:
            input_value = self.request.session.get(param)
            if input_value:
                standard_value_param = getattr(standard_value, param)
                threshold = thresholds.get(param)
                if standard_value_param and threshold:
                    diff = abs(float(input_value) - standard_value_param)
                    if diff > threshold.reference_value_threshold:
                        context['alerts'][param] = "基準値の範囲を超えています"

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