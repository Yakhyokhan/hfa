from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserWithInfo

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = UserWithInfo
        fields = ['username','first_name', 'last_name', 'tel_num']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UserWithInfo
        fields = ['username','first_name', 'last_name', 'tel_num']
