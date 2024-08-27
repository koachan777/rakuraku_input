from django.views.generic import TemplateView
from django.db.models import Q

from rakuraku_apps.models import ShrimpModel, WaterQualityModel, TankModel

class TableOrGraphView(TemplateView):
    template_name = 'log/table_or_graph.html'

from django.views.generic import TemplateView
from django.db.models import Q
from rakuraku_apps.models import WaterQualityModel, TankModel, ShrimpModel

class TableView(TemplateView):
    template_name = 'log/table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        shrimp_id = self.request.GET.get('shrimp')
        item = self.request.GET.get('item')

        query = Q()
        if start_date and end_date:
            query &= Q(date__range=[start_date, end_date])
        if shrimp_id:
            query &= Q(tank__shrimp__id=shrimp_id)

        water_quality_data = WaterQualityModel.objects.filter(query).select_related('tank', 'tank__shrimp')

        if item:
            water_quality_data = water_quality_data.values('date', 'tank__name', item)
        else:
            water_quality_data = water_quality_data.values('date', 'tank__name', 'pH', 'DO', 'salinity', 'NH4', 'NO2', 'NO3', 'Ca', 'Al', 'Mg')

        # 日付の昇順と水槽IDの昇順で並び替え
        water_quality_data = water_quality_data.order_by('date', 'tank__id')

        context['water_quality_data'] = water_quality_data
        context['shrimps'] = ShrimpModel.objects.all()
        return context

class GraphView(TemplateView):
    template_name = 'log/graph.html'