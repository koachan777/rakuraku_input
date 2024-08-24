from django.views.generic import TemplateView

class IntervalFirstInputView(TemplateView):
    template_name = 'input/interval/first_input.html'

class IntervalSecondInputView(TemplateView):
    template_name = 'input/interval/second_input.html'

class IntervalThirdInputView(TemplateView):
    template_name = 'input/interval/third_input.html'

class IntervalCommentInputView(TemplateView):
    template_name = 'input/interval/comment_input.html'

class IntervalConfirmInputView(TemplateView):
    template_name = 'input/interval/confirm.html'

class IntervalEditView(TemplateView):
    template_name = 'input/interval/edit.html'
