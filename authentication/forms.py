from django.contrib.auth.forms import UserCreationForm

from authentication.models import CRMUser


class MyUserCreationForm(UserCreationForm):

    class Meta:
        model = CRMUser
        fields = '__all__'
