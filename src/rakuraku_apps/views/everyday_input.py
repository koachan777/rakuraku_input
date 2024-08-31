from datetime import date, datetime, timedelta

from django.utils import timezone
from django.views.generic import TemplateView
from django.shortcuts import redirect
from rakuraku_apps.models import StandardValueModel, TankModel, WaterQualityModel, WaterQualityThresholdModel
from rakuraku_apps.forms.input import WaterQualityForm

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
        
        # 過去のデータの表示
        # セッションデータから日付とタンクIDを取得
        current_date = timezone.datetime.strptime(self.request.session.get('date', ''), '%Y-%m-%d').date()
        tank_id = self.request.session.get('tank', '')

        # 過去のデータを取得
        previous_data = {
            '1日前': WaterQualityModel.objects.filter(date=current_date - timedelta(days=1), tank_id=tank_id).first(),
            '2日前': WaterQualityModel.objects.filter(date=current_date - timedelta(days=2), tank_id=tank_id).first(),
            '7日前': WaterQualityModel.objects.filter(date=current_date - timedelta(days=7), tank_id=tank_id).first(),
            '14日前': WaterQualityModel.objects.filter(date=current_date - timedelta(days=14), tank_id=tank_id).first(),
            '1か月前': WaterQualityModel.objects.filter(date=current_date - timedelta(days=30), tank_id=tank_id).first(),
            '1年前': WaterQualityModel.objects.filter(date=current_date - timedelta(days=365), tank_id=tank_id).first(),
        }

        # 結果を表示
        # print("previous_data", previous_data)
        
        context['previous_data'] = previous_data       


        # 基準値を取得
        # standard_value = StandardValueModel.get_or_create()

        # 閾値を取得
        thresholds = {t.parameter: t for t in WaterQualityThresholdModel.objects.all()}

        # アラートメッセージを格納する辞書
        context['alerts'] = {}
        
        # print("standard_value", standard_value)
        print("thresholds", thresholds)

        # 各パラメーターについて基準値と比較
        for param in ['water_temperature', 'pH', 'DO', 'salinity', 'NH4', 'NO2', 'NO3', 'Ca', 'Al', 'Mg']:
            input_value = self.request.session.get(param)
            if input_value:
                threshold = thresholds.get(param)
                print(f"{param} : {input_value} min : {threshold.reference_value_threshold_min} max : {threshold.reference_value_threshold_max} range : {threshold.reference_value_threshold_range} previous_day_threshold : {threshold.previous_day_threshold} ")
                
                context['alerts'][param] = ""
                
                previous_value = getattr(previous_data['1日前'], param, None)
                if previous_value is not None and input_value is not None:
                    if abs(float(previous_value) - float(input_value)) > threshold.previous_day_threshold:
                        _arrow = ''
                        if float(previous_value) - float(input_value) > 0:
                            _arrow = '↓'    
                        else:
                            _arrow = '↑'
                        context['alerts'][param] = {'previous_day_threshold': f"昨日から{round(abs(float(previous_value) - float(input_value)), 2)}{_arrow}"}
                        
                         
                
                # 基準値の最小値と最大値が同じ場合 → 基準値が一つの場合のもの
                if threshold.reference_value_threshold_min == threshold.reference_value_threshold_max:
                    try:
                        if float(input_value) < threshold.reference_value_threshold_range - threshold.reference_value_threshold_min:
                            context['alerts'][param] = {"reference_value_threshold_min": "基準値以下"}
                        elif float(input_value) > threshold.reference_value_threshold_range + threshold.reference_value_threshold_min:
                            context['alerts'][param] = {"reference_value_threshold_max": "基準値以上"}
                    except:
                        pass
                        # おそらくmin, max, rangeがNoneの場合でうまく処理できていないとき，例外処理を何にするかは未定
                
                # 基準値の最小値と最大値が異なる場合
                else:
                    if threshold.reference_value_threshold_min != None and float(input_value) < threshold.reference_value_threshold_min:
                        context['alerts'][param] = {"reference_value_threshold_min": "基準値以下"}
                    elif threshold.reference_value_threshold_max != None and float(input_value) > threshold.reference_value_threshold_max:
                        context['alerts'][param] = {"reference_value_threshold_max": "基準値以上"}
                
                        
        # print("context", context)

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

            #ライン通知する際はコメントアウトを外す
            # アラートが発生していた場合、LINEグループに通知を送信
            # context = self.get_context_data()
            # if context['alerts']:
            #     self.send_line_notify(context['alerts'], context['form_data'])

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


    #ライン通知する際はコメントアウトを外す
    # def send_line_notify(self, alerts, form_data):
    #     line_notify_token = ''  # LINEグループ用のアクセストークンを設定
    #     line_notify_api = 'https://notify-api.line.me/api/notify'

    #     # 文字列から日付型に変換する
    #     date_obj = datetime.strptime(form_data['date'], '%Y-%m-%d')
    #     date_str = date_obj.strftime('%Y年%m月%d日')
    #     alert_message = f"{date_str}\n\n"

    #     if 'water_temperature' in alerts:
    #         alert_message += f"水温: {form_data['water_temperature']}℃\n"
    #         alert_message += f"{alerts['water_temperature']}\n\n"

    #     if 'pH' in alerts:
    #         alert_message += f"pH: {form_data['pH']}\n"
    #         alert_message += f"{alerts['pH']}\n\n"

    #     if 'DO' in alerts:
    #         alert_message += f"DO: {form_data['DO']} mg/L\n"
    #         alert_message += f"{alerts['DO']}\n\n"

    #     if 'salinity' in alerts:
    #         alert_message += f"塩分濃度: {form_data['salinity']} %\n"
    #         alert_message += f"{alerts['salinity']}\n\n"

    #     payload = {'message': alert_message.strip()}
    #     headers = {'Authorization': f'Bearer {line_notify_token}'}

    #     requests.post(line_notify_api, data=payload, headers=headers)

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