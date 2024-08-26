from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, UpdateView
from rakuraku_apps.models import TankModel, WaterQualityModel
from rakuraku_apps.forms.input import WaterQualityForm
from rakuraku_apps.forms.input import WaterQualityForm
from rakuraku_apps.models import TankModel, WaterQualityModel
from datetime import date


class EverydayOrIntervalView(TemplateView):
    template_name = 'input/evryday_or_interval.html'

class EverydayFirstInputView(TemplateView):
    template_name = 'input/everyday/first_input.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tanks'] = TankModel.objects.all()
        context['today'] = date.today().strftime('%Y-%m-%d')

        return context

    def post(self, request, *args, **kwargs):
        request.session['date'] = request.POST['date']
        request.session['tank'] = request.POST['tank']
        request.session['room_temperature'] = request.POST['room_temperature']
        return redirect('/everyday/second_input/')

class EverydaySecondInputView(TemplateView):
    template_name = 'input/everyday/second_input.html'

    def post(self, request, *args, **kwargs):
        request.session['water_temperature'] = request.POST['water_temperature']
        request.session['pH'] = request.POST['pH']
        request.session['DO'] = request.POST['DO']
        request.session['salinity'] = request.POST['salinity']
        return redirect('/everyday/comment/')

class EverydayCommentInputView(TemplateView):
    template_name = 'input/everyday/comment_input.html'

    def post(self, request, *args, **kwargs):
        request.session['notes'] = request.POST['notes']
        return redirect('/everyday/confirm/')

class EverydayConfirmInputView(TemplateView):
    template_name = 'input/everyday/confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_data'] = {
            'date': self.request.session.get('date', ''),
            'tank': self.request.session.get('tank', ''),
            'room_temperature': self.request.session.get('room_temperature', ''),
            'water_temperature': self.request.session.get('water_temperature', ''),
            'pH': self.request.session.get('pH', ''),
            'DO': self.request.session.get('DO', ''),
            'salinity': self.request.session.get('salinity', ''),
            'notes': self.request.session.get('notes', ''),
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
        form = WaterQualityForm(form_data)
        if form.is_valid():
            form.save()
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
            form.save()
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
            return self.render_to_response(self.get_context_data(form=form))