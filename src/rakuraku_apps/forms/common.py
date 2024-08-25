from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from rakuraku_apps.models import User



class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "account_id",
        )

class LoginForm(AuthenticationForm):
    class Meta:
        model = User