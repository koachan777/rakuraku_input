from django.views.generic import TemplateView

class EverydayOrIntervalView(TemplateView):
    template_name = 'input/evryday_or_interval.html'

class EverydayFirstInputView(TemplateView):
    template_name = 'input/everyday/first_input.html'

class EverydaySecondInputView(TemplateView):
    template_name = 'input/everyday/second_input.html'

class EverydayCommentInputView(TemplateView):
    template_name = 'input/everyday/comment_input.html'

class EverydayConfirmInputView(TemplateView):
    template_name = 'input/everyday/confirm.html'

class EverydayEditView(TemplateView):
    template_name = 'input/everyday/edit.html'
    
