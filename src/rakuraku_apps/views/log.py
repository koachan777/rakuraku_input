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
        water_quality_data = water_quality_data.order_by('tank__name', 'date')

        context['water_quality_data'] = water_quality_data
        context['shrimps'] = ShrimpModel.objects.all()
        context['start_date'] = start_date
        context['end_date'] = end_date

        return context

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
            water_quality_data = water_quality_data.values('date', 'tank__name', item)
        else:
            item = 'water_temperature'  # デフォルトの項目をwater_temperatureに設定
            water_quality_data = water_quality_data.values('date', 'tank__name', item)

        water_quality_data = water_quality_data.order_by('date', 'tank__id')

        # グラフの描画
        fig, ax = plt.subplots(figsize=(10, 6), tight_layout=True)
        fig.subplots_adjust(top=0.9)
        fig.suptitle(item_labels.get(item, ''), fontsize=24, fontweight='bold')  # タイトルの文字サイズを24に変更し、太字に設定
        tanks = water_quality_data.values_list('tank__name', flat=True).distinct()
        tank_labels = []
        for tank in tanks:
            tank_data = water_quality_data.filter(tank__name=tank)
            dates = [data['date'] for data in tank_data]
            values = [data[item] for data in tank_data]
            label = tank.split()[0]
            if label not in tank_labels:
                ax.plot(dates, values, marker='o', label=label)
                tank_labels.append(label)
            else:
                ax.plot(dates, values, marker='o')

        ax.set_xlabel('')  # x軸のラベルを削除
        ax.legend(loc='upper right')  # 凡例の位置を右上に変更
        ax.xaxis.set_major_formatter(DateFormatter('%m/%d'))  # 日付のフォーマットを変更
        ax.xaxis.set_major_locator(DayLocator(interval=1))  # x軸の目盛りを1日ごとに設定
        fig.autofmt_xdate()

        # y軸の値の横に線を追加
        ax.grid(axis='y', linestyle='-', linewidth=0.5, color='gray', alpha=0.7)


        # グラフをbase64エンコードされた文字列に変換
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        graph = base64.b64encode(image_png).decode('utf-8')
        buffer.close()

        context['graph'] = graph
        context['shrimps'] = ShrimpModel.objects.all()
        context['selected_item'] = item_labels.get(item, '')  # 選択された項目名を日本語に変換
        context['start_date'] = start_date
        context['end_date'] = end_date
        return context