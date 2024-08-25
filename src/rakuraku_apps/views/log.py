from django.views.generic import TemplateView

class TableOrGraphView(TemplateView):
    template_name = 'log/table_or_graph.html'

class TableView(TemplateView):
    template_name = 'log/table.html'

class GraphView(TemplateView):
    template_name = 'log/graph.html'