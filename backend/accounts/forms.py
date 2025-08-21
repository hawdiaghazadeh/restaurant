from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from .models import User

class UserCreationForm(BaseUserCreationForm):

    class meta :
        model = User
        fields = ['email', 'first_name', 'last_name']