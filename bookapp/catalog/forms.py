from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from .models import UserProfile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2'
                  )


def save(self, commit=True):
    user = super(RegistrationForm, self).save(commit=False)
    user.first_name = cleaned_data['first_name']
    user.last_name = cleaned_data['last_name']
    user.email = cleaned_data['email']

    if commit:
        user.save()


class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = {
            'email',
            'first_name',
            'last_name',
        }
        exclude = {
            'password',
        }
        field_order = ['email', 'first_name', 'last_name']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = {
            'address',
            'city',
            'state',
            'zipcode',
        }
        exclude = {
            'password',
        }

        field_order = ['address', 'city', 'state', 'zipcode']
