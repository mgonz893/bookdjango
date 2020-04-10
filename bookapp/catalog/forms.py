from django import forms
from django.forms import Textarea
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from .models import UserProfile, BookRating, ShippingAddr, Wishlist, CreditCard


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
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'Password must contain at least 8 characters. Cannot be entirely numeric.'
        

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
            'nickname',
            'address',
            'city',
            'state',
            'zipcode',
        }
        exclude = {
            'password',
        }

        field_order = ['nickname','address', 'city', 'state', 'zipcode']


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddr
        fields = {
            'address',
            'city',
            'state',
            'zipcode',
        }
        exclude = {
            'username',
        }
        field_order = ['address', 'city', 'state', 'zipcode']


class CreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = {
            'ccnumber',
            'ccv',
            'expiration',
        }
        exclude = {
            'username',
        }
        field_order = ['ccnumber', 'ccv', 'expiration']


class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs['readonly'] = True
        self.fields['book'].widget.attrs['readonly'] = True

    class Meta:
        model = BookRating
        widgets = {'book': forms.HiddenInput(), 'user': forms.HiddenInput()}
        fields = {
            'book', 'user', 'rating', 'review', 'anonymous'
        }
        field_order = ['book', 'user', 'rating', 'review', 'anonymous']


class WishForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = {
            'name',
        }
        exclude = {
            'user',
        }
