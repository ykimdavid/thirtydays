from django.db import models
from django.contrib.auth.models import User
from django.forms import EmailField
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
        }

# Create your models here.
