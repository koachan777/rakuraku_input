import datetime
from django.views.generic import TemplateView
from django.db.models import Q

from rakuraku_apps.models import ShrimpModel, WaterQualityModel, TankModel
import io
import base64
from django.views.generic import TemplateView
from django.db.models import Q
from rakuraku_apps.models import WaterQualityModel, TankModel, ShrimpModel
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import japanize_matplotlib
from matplotlib.dates import DateFormatter, DayLocator
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, redirect
from rakuraku_apps.forms.log import WaterQualityEditForm



class TableOrGraphView(TemplateView):
    template_name = 'log/table_or_graph.html'


from datetime import datetime, timedelta

class TableView(TemplateView):
    template_name = 'log/table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        shrimp_id = self.request.GET.get('shrimp')
        item = self.request.GET.get('item')

        if not start_date:
            start_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.today().strftime('%Y-%m-%d')

        query = Q(date__range=[start_date, end_date])

        if shrimp_id:
            query &= Q(tank__shrimp__id=shrimp_id)

        water_quality_data = WaterQualityModel.objects.filter(query).select_related('tank', 'tank__shrimp')

        if item:
            water_quality_data = water_quality_data.values('date', 'tank__name', item).order_by('date', 'tank__name')
            water_quality_data_by_date = {}
            for data in water_quality_data:
                date = data['date']
                tank_name = data['tank__name']
                value = data[item]
                if date not in water_quality_data_by_date:
                    water_quality_data_by_date[date] = {}
                water_quality_data_by_date[date][tank_name] = value
            context['water_quality_data_by_date'] = dict(sorted(water_quality_data_by_date.items()))
            
            if shrimp_id:
                context['tanks'] = TankModel.objects.filter(shrimp__id=shrimp_id, water_quality__date__range=[start_date, end_date]).distinct()
            else:
                context['tanks'] = TankModel.objects.filter(water_quality__date__range=[start_date, end_date]).distinct()
        else:
            water_quality_data = water_quality_data.values('date', 'tank__name', 'pH', 'DO', 'salinity', 'NH4', 'NO2', 'NO3', 'Ca', 'Al', 'Mg', 'water_temperature', 'room_temperature', 'notes')

        # 水槽名の昇順と日付の昇順で並び替え
        water_quality_data = water_quality_data.order_by('tank__name', 'date').values('id', 'date', 'tank__name', 'pH', 'DO', 'salinity', 'NH4', 'NO2', 'NO3', 'Ca', 'Al', 'Mg', 'water_temperature', 'room_temperature', 'notes')
        context['water_quality_data'] = water_quality_data
        context['shrimps'] = ShrimpModel.objects.all()
        context['start_date'] = start_date
        context['end_date'] = end_date

        return context
    
def edit_water_quality(request, pk):
    water_quality = get_object_or_404(WaterQualityModel, pk=pk)
    if request.method == 'POST':
        form = WaterQualityEditForm(request.POST, instance=water_quality)
        if form.is_valid():
            form.save()
            return redirect('rakuraku_apps:table')
    else:
        form = WaterQualityEditForm(instance=water_quality)
    return render(request, 'log/edit_water_quality.html', {'form': form})

def delete_water_quality(request, pk):
    water_quality = get_object_or_404(WaterQualityModel, pk=pk)
    if request.method == 'POST':
        water_quality.delete()
    return redirect('rakuraku_apps:table')

class GraphView(TemplateView):
    template_name = 'log/graph.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        shrimp_id = self.request.GET.get('shrimp')
        item = self.request.GET.get('item')
        if not start_date:
            start_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.today().strftime('%Y-%m-%d')

        item_labels = {
            'water_temperature': '水温',
            'pH': 'pH',
            'DO': 'DO',
            'salinity': '塩分濃度',
            'NH4': 'NH4',
            'NO2': 'NO2',
            'NO3': 'NO3',
            'Ca': 'Ca',
            'Al': 'Al',
            'Mg': 'Mg'
        }

        query = Q()
        if start_date and end_date:
            query &= Q(date__range=[start_date, end_date])
        if shrimp_id:
            query &= Q(tank__shrimp__id=shrimp_id)

        water_quality_data = WaterQualityModel.objects.filter(query).select_related('tank', 'tank__shrimp')

        if item:
            water_quality_data = water_quality_data.values('date', 'tank__name', 'tank__shrimp__id', item)
        else:
            item = 'water_temperature'  # デフォルトの項目をwater_temperatureに設定
            water_quality_data = water_quality_data.values('date', 'tank__name', 'tank__shrimp__id', item)

        water_quality_data = water_quality_data.order_by('date', 'tank__id')

        # グラフの描画
        fig, ax = plt.subplots(figsize=(10, 6), tight_layout=True)
        fig.subplots_adjust(top=0.9)
        fig.suptitle(item_labels.get(item, ''), fontsize=24, fontweight='bold')

        # 系統ごとに水槽をグルーピング
        shrimp_tanks = {}
        for tank_data in water_quality_data:
            shrimp_id = tank_data.get('tank__shrimp__id')
            if shrimp_id:
                if shrimp_id not in shrimp_tanks:
                    shrimp_tanks[shrimp_id] = []
                shrimp_tanks[shrimp_id].append(tank_data)

        colors = plt.cm.get_cmap('tab20', sum(len(set(tank['tank__name'] for tank in tanks)) for tanks in shrimp_tanks.values()))
        color_index = 0

        for shrimp_id, tanks in shrimp_tanks.items():
            # 系統内の水槽をID順にソート
            tanks.sort(key=lambda x: x['tank__name'])

            # 重複する水槽名を解消
            unique_tank_names = sorted(set(tank['tank__name'] for tank in tanks))

            for tank_name in unique_tank_names:
                dates = [data['date'] for data in water_quality_data if data['tank__name'] == tank_name]
                values = [data[item] for data in water_quality_data if data['tank__name'] == tank_name]

                color = colors(color_index)
                ax.plot(dates, values, marker='o', label=tank_name, color=color, linewidth=2)
                color_index += 1

        # 凡例の表示
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels, loc='upper right')

        # 日付の間隔を計算
        num_days = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days + 1
        if num_days > 20:
            interval = 5
        else:
            interval = 1

        # 年をまたぐかどうかを判定
        start_year = datetime.strptime(start_date, '%Y-%m-%d').year
        end_year = datetime.strptime(end_date, '%Y-%m-%d').year
        if start_year != end_year:
            date_format = '%Y/%m/%d'
        else:
            date_format = '%m/%d'


        ax.xaxis.set_major_formatter(DateFormatter(date_format))
        ax.xaxis.set_major_locator(DayLocator(interval=interval))
        fig.autofmt_xdate()
        ax.grid(axis='y', linestyle='-', linewidth=0.5, color='gray', alpha=0.7)

        # 単位を設定
        unit = ''
        if item == 'water_temperature':
            unit = '°C'
        elif item == 'DO':
            unit = 'mg/L'
        elif item == 'salinity':
            unit = '%'
        elif item in ['NH4', 'NO2', 'NO3', 'Ca', 'Al', 'Mg']:
            unit = 'mg/L'

        # 単位がある場合のみ、グラフの枠の外の左上に表示
        if unit:
            plt.figtext(0.03, 0.925, f'({unit})', fontsize=12, bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))


        # グラフをbase64エンコードされた文字列に変換
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        graph = base64.b64encode(image_png).decode('utf-8')
        buffer.close()

        context['graph'] = graph
        context['shrimps'] = ShrimpModel.objects.all()
        context['selected_item'] = item  # 選択された項目をそのまま渡す
        context['start_date'] = start_date
        context['end_date'] = end_date
        return context