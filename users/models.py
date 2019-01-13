from django.db import models
from django.contrib.auth.models import User
from django.forms import EmailField, ModelForm, CharField
from django.contrib.auth.forms import UserCreationForm
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)




class RegistrationForm(UserCreationForm):
    email = EmailField(required=True)
    name = CharField(max_length=100)
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']
        help_texts = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
        }

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        name = self.cleaned_data['name']

        if commit:
            user.save()
            profile = Profile.objects.create(user = user, name = name)
            profile.save()
        return user

class UserUpdateForm(ModelForm):
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']
        help_texts = {
            'username' : None
        }

class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'image']
# Create your models here.
