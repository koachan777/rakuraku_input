from django.views.generic import TemplateView

class ManageView(TemplateView):
    template_name = 'manage/manage.html'

class ManageUserView(TemplateView):
    template_name = 'manage/user.html'

class ManageTankView(TemplateView):
    template_name = 'manage/tank.html'

class ManagValueView(TemplateView):
    template_name = 'manage/value.html'

class ManageFirstAlertView(TemplateView):
    template_name = 'manage/first_alert.html'

class ManageSecondAlertView(TemplateView):
    template_name = 'manage/second_alert.html'