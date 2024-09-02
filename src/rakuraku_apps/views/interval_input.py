from datetime import date

from django.shortcuts import redirect
from django.views.generic import TemplateView
from rakuraku_apps.forms.input import IntervalWaterQualityForm
from rakuraku_apps.models import TankModel, WaterQualityModel, WaterQualityThresholdModel



class IntervalFirstInputView(TemplateView):
    template_name = 'input/interval/first_input.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        print("context",context)
        
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
                    
                    'NH4': water_quality.NH4,
                    'NO2': water_quality.NO2,
                    'NO3': water_quality.NO3,
                    
                    'Ca': water_quality.Ca,
                    'Al': water_quality.Al,
                    'Mg': water_quality.Mg,
                    
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
            
            request.session['NH4'] = water_quality.NH4 or ''
            request.session['NO2'] = water_quality.NO2 or ''
            request.session['NO3'] = water_quality.NO3 or ''
            
            request.session['Ca'] = water_quality.Ca or ''
            request.session['Al'] = water_quality.Al or ''
            request.session['Mg'] = water_quality.Mg or ''
            
            request.session['notes'] = water_quality.notes or ''
        else:
            request.session['water_quality_id'] = None
            request.session['date'] = date_str
            request.session['tank'] = tank_id
            request.session['room_temperature'] = room_temperature
            
            request.session['NH4'] = ''
            request.session['NO2'] = ''
            request.session['NO3'] = ''
            
            request.session['Ca'] = ''
            request.session['Al'] = ''
            request.session['Mg'] = ''
            
            request.session['notes'] = ''
            
        return redirect('/interval/second_input/')

class IntervalSecondInputView(TemplateView):
    template_name = 'input/interval/second_input.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_data'] = {
            'NH4': self.request.session.get('NH4', ''),
            'NO2': self.request.session.get('NO2', ''),
            'NO3': self.request.session.get('NO3', ''),
        }
        return context

    def post(self, request, *args, **kwargs):
        request.session['NH4'] = request.POST['NH4']
        request.session['NO2'] = request.POST['NO2']
        request.session['NO3'] = request.POST['NO3']
        return redirect('/interval/third_input/')

class IntervalThirdInputView(TemplateView):
    template_name = 'input/interval/third_input.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_data'] = {
            'Ca': self.request.session.get('Ca', ''),
            'Al': self.request.session.get('Al', ''),
            'Mg': self.request.session.get('Mg', ''),
        }
        return context

    def post(self, request, *args, **kwargs):
        request.session['Ca'] = request.POST['Ca']
        request.session['Al'] = request.POST['Al']
        request.session['Mg'] = request.POST['Mg']
        return redirect('/interval/comment/')

class IntervalCommentInputView(TemplateView):
    template_name = 'input/interval/comment_input.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_data'] = {
            'notes': self.request.session.get('notes', ''),
        }
        return context

    def post(self, request, *args, **kwargs):
        request.session['notes'] = request.POST['notes']
        return redirect('/interval/confirm/')

class IntervalConfirmInputView(TemplateView):
    template_name = 'input/interval/confirm.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tank_id = self.request.session.get('tank', '')
        tank = TankModel.objects.get(pk=tank_id)
        context['form_data'] = {
            'date': self.request.session.get('date', ''),
            'tank': tank.name,
            'room_temperature': self.request.session.get('room_temperature', ''),
            'NH4': self.request.session.get('NH4', ''),
            'NO2': self.request.session.get('NO2', ''),
            'NO3': self.request.session.get('NO3', ''),
            'Ca': self.request.session.get('Ca', ''),
            'Al': self.request.session.get('Al', ''),
            'Mg': self.request.session.get('Mg', ''),
            'notes': self.request.session.get('notes', ''),
        }

        # 基準値を取得
        # standard_value = StandardValueModel.get_or_create()

        # 閾値を取得
        # thresholds = {t.parameter: t for t in WaterQualityThresholdModel.objects.all()}

        # # アラートメッセージを格納する辞書
        # context['alerts'] = {}

        # # 各パラメーターについて基準値と比較
        # for param in ['water_temperature', 'pH', 'DO', 'salinity', 'NH4', 'NO2', 'NO3', 'Ca', 'Al', 'Mg']:
        #     input_value = self.request.session.get(param)
        #     if input_value:
        #         standard_value_param = getattr(standard_value, param)
        #         threshold = thresholds.get(param)
        #         if input_value and standard_value_param is not None and threshold is not None:
        #             diff = abs(float(input_value) - standard_value_param)
        #             if threshold.reference_value_threshold is not None and diff > threshold.reference_value_threshold:
        #                 context['alerts'][param] = "基準値の範囲を超えています"

        return context

    def post(self, request, *args, **kwargs):
        form_data = {
            'date': request.session['date'],
            'tank': request.session['tank'],
            'room_temperature': request.session['room_temperature'],
            'NH4': request.session['NH4'],
            'NO2': request.session['NO2'],
            'NO3': request.session['NO3'],
            'Ca': request.session['Ca'],
            'Al': request.session['Al'],
            'Mg': request.session['Mg'],
            'notes': request.session['notes'],
        }

        water_quality_id = request.session.get('water_quality_id')
        if water_quality_id:
            water_quality = WaterQualityModel.objects.get(id=water_quality_id)
            form = IntervalWaterQualityForm(form_data, instance=water_quality)
        else:
            form = IntervalWaterQualityForm(form_data)

        if form.is_valid():
            form.save()
            request.session.pop('water_quality_id', None)
            request.session.pop('date', None)
            request.session.pop('tank', None)
            request.session.pop('room_temperature', None)
            request.session.pop('NH4', None)
            request.session.pop('NO2', None)
            request.session.pop('NO3', None)
            request.session.pop('Ca', None)
            request.session.pop('Al', None)
            request.session.pop('Mg', None)
            request.session.pop('notes', None)
            request.session['success_message'] = '測定結果を保存しました'
            return redirect('/home/')
        else:
            return redirect('/interval/edit/')

class IntervalEditView(TemplateView):
    template_name = 'input/interval/edit.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = IntervalWaterQualityForm(initial={
            'date': self.request.session.get('date', ''),
            'tank': self.request.session.get('tank', ''),
            'room_temperature': self.request.session.get('room_temperature', ''),
            'NH4': self.request.session.get('NH4', ''),
            'NO2': self.request.session.get('NO2', ''),
            'NO3': self.request.session.get('NO3', ''),
            'Ca': self.request.session.get('Ca', ''),
            'Al': self.request.session.get('Al', ''),
            'Mg': self.request.session.get('Mg', ''),
            'notes': self.request.session.get('notes', ''),
        })
        return context

    def post(self, request, *args, **kwargs):
        form = IntervalWaterQualityForm(request.POST)
        if form.is_valid():
            request.session['date'] = form.cleaned_data['date'].strftime('%Y-%m-%d')
            request.session['tank'] = form.cleaned_data['tank'].pk  # 変更
            request.session['room_temperature'] = form.cleaned_data['room_temperature']
            request.session['NH4'] = form.cleaned_data['NH4']
            request.session['NO2'] = form.cleaned_data['NO2']
            request.session['NO3'] = form.cleaned_data['NO3']
            request.session['Ca'] = form.cleaned_data['Ca']
            request.session['Al'] = form.cleaned_data['Al']
            request.session['Mg'] = form.cleaned_data['Mg']
            request.session['notes'] = form.cleaned_data['notes']
            return redirect('/interval/confirm/')
        else:
            return self.render_to_response(self.get_context_data(form=form))
